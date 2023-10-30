import collections

from gopro_overlay.ffmpeg_gopro import DataStream
from gopro_overlay.timeunits import timeunits


class StreamFindingVisitor:

    def __init__(self, wanted):
        self.wanted = wanted
        self._found = False

    def vic_DEVC(self, item, contents):
        return self

    def vic_STRM(self, item, contents):
        if self.wanted in contents:
            self._found = True

    def found(self):
        return self._found

    def v_end(self):
        pass


class DetermineTimestampOfFirstSHUTVisitor:
    """
        Seems like first SHUT frame is correlated with video frame?
        https://github.com/gopro/gpmf-parser/blob/151bb352ab3d1af8feb31e0cf8277ff86c70095d/demo/GPMF_demo.c#L414
    """

    def __init__(self):
        self._initial_timestamp = None

    @property
    def timestamp(self):
        return self._initial_timestamp

    def vic_DEVC(self, item, contents):
        if not self._initial_timestamp:
            return self

    def vi_STMP(self, item):
        self._initial_timestamp = item.interpret()

    def vic_STRM(self, item, contents):
        if "SHUT" in contents and not self._initial_timestamp:
            return self

    def v_end(self):
        pass


class PayloadMaths:
    def __init__(self, datastream: DataStream):
        self._datastream = datastream
        self._max_time = datastream.frame_count * datastream.frame_duration / datastream.timebase

    def time_of_out_packet(self, packet_number):
        packet_time = (packet_number + 1) * self._datastream.frame_duration / self._datastream.timebase
        return min(packet_time, self._max_time)


CorrectionFactors = collections.namedtuple("CorrectionFactors", ["first_frame", "last_frame", "frames_s"])


class CalculateCorrectionFactorsVisitor:
    """This implements GetGPMFSampleRate in GPMF_utils.c"""

    def __init__(self, wanted: str, metameta: DataStream):
        self.wanted = wanted
        self.wanted_method_name = f"vi_{self.wanted}"
        self._payload_maths = PayloadMaths(metameta)
        self.count = 0
        self.samples = 0
        self.meanY = 0
        self.meanX = 0
        self.repeatarray = []

    def vic_DEVC(self, item, contents):
        return self

    def __getattr__(self, name, *args):
        if name == self.wanted_method_name:
            return self._handle_item
        else:
            raise AttributeError(f"{name}")

    def vic_STRM(self, item, contents):
        if self.wanted in contents:
            return self

    def _handle_item(self, item):
        self.samples += item.repeat
        self.meanY += self.samples
        self.meanX += self._payload_maths.time_of_out_packet(self.count)
        self.repeatarray.append(self.samples)
        self.count += 1

    def v_end(self):
        pass

    def found(self) -> bool:
        """indicate if we found any of the requested packet. might be one that's not present in this stream"""
        return self.count > 0

    # no idea how this works, but the numbers that come out of it are the same numbers as in GPMF_utils.c
    def factors(self):
        meanY = self.meanY / self.count
        meanX = self.meanX / self.count

        top = 0
        bottom = 0
        for index, sample in enumerate(self.repeatarray):
            time_of_out_packet = self._payload_maths.time_of_out_packet(index)
            top += (time_of_out_packet - meanX) * (sample - meanY)
            bottom += (time_of_out_packet - meanX) * (time_of_out_packet - meanX)

        slope = top / bottom
        rate = slope

        intercept = meanY - slope * meanX
        first = -intercept / rate
        last = first + self.samples / rate

        return CorrectionFactors(
            first_frame=timeunits(seconds=first),
            last_frame=timeunits(seconds=last),
            frames_s=rate
        )
