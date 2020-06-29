import json
from time import time

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, 'api/index.html')


def get_bandwidths_from_disk(device_id: str, end_time: float, window_time: int, num_windows: int):
    with open("bandwidths_by_device.json") as f:
        # get device's bandwidths (already sorted by timestamp in descending order)
        device_bandwidths = json.load(f)[device_id]

        bytes_ts_res = []
        bytes_fs_res = []
        window_ends = []

        window_start_time = end_time
        i = 0

        # for as many windows as requested
        for _ in range(num_windows):
            # iterate over bandwidths, creating sums of bandwidth_to and bandwidth_from

            # find next start and end time based on window size
            window_end_time = window_start_time
            window_start_time = window_end_time - window_time
            bytes_ts = 0
            bytes_fs = 0

            # skip any bandwidths that are too late
            if i < len(device_bandwidths) and device_bandwidths[i]["timestamp"] > window_end_time:
                i += 1

            if i < len(device_bandwidths) and device_bandwidths[i]["timestamp"] > window_start_time:
                bytes_ts += device_bandwidths[i]["bytes_ts"]
                bytes_fs += device_bandwidths[i]["bytes_fs"]
                i += 1

            bytes_ts_res.append(bytes_ts)
            bytes_fs_res.append(bytes_fs)
            window_ends.append(window_end_time)

        bytes_ts_res.reverse()
        bytes_fs_res.reverse()
        window_ends.reverse()

        return {"bytes_ts": bytes_ts_res, "bytes_fs": bytes_fs_res, "window_ends": window_ends}


def get_bandwidths(request):
    device_id = request.GET.get('device_id', None)
    if not device_id:
        return HttpResponseBadRequest('Must provide device_id.')
    end_time = request.GET.get('end_time', time())
    window_time = request.GET.get('window_time', 60)
    num_windows = request.GET.get('num_windows', 10)

    # return data
    bandwidths = get_bandwidths_from_disk(
        device_id, float(end_time), window_time, num_windows)
    return JsonResponse(bandwidths)
