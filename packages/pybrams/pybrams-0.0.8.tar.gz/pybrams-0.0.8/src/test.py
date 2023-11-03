from brams import enable_cache, disable_cache, clear_cache
from brams import locations
from brams import systems
from brams import files
from brams import cache
import json
import timeit



enable_cache()

f = files.get("2023-09-02T23:55", "BEBILZ_SYS001")
f.load()
f.process()

# f = files.get("2023-09-02T23:59:34/2023-09-03T00:00:15", ["BEOTTI_SYS001"])
# print(f)
# f1, f2 = f["BEOTTI_SYS001"]
# print(json.dumps(f1, indent=4))
# print(json.dumps(f2, indent=4))


# f3 = f1 + f2
# print(json.dumps(f3, indent=4))
# print(f1.precise_end)
# print(f2.precise_start)
# print(f2.precise_start - f1.precise_end)



# f2 = files.get("2010-10-23T00:05", "FREPIN_SYS001")
# f1.load()
# f2.load()
# print(json.dumps(f1, indent=4))
# print(json.dumps(f2, indent=4))
# print(len(f1.signal.data))
# print(len(f2.signal.data))
# print(len(f1.pps.timestamps.data))
# print(len(f2.pps.timestamps.data))

# fs1 = f1.sample_rate
# fs2 = f2.sample_rate

# print((2756.25 / fs1) - (2756.25 / fs2))

# systems.all()
#systems.get(location="BEHUMA")
# systems.get(location="BEOTTI")

# systems.get(system_code="BEHUMA_SYS004")




# clear_cache()
# enable_cache()

#print(json.dumps(files.get("2023-01-01T00:00", ["BEBILZ_SYS001", "BEHUMA_SYS002", "NLMAAS_SYS001"]), indent=4))


# enable_cache()

# print("clearing cache")
# # clearing cache
# clear_cache()

# start = timeit.default_timer()

# f = files.get("2023-01-01T00:00", "BEBILZ_SYS001")
# for i in range (40):
    
#     f.load()

# print(timeit.default_timer() - start)



# print("downloading and caching")
# # caching the file after downloading it
# file = files.get("2023-01-01T00:00", "BEBILZ_SYS001")
# file.load()


# print("getting file out of the cache")
# # getting file out of cache
# cached_file = files.get("2023-01-01T00:00", "BEBILZ_SYS001")
# cached_file.load()

# print("disabling cache")
# # disabling cache
# disable_cache()

# print("downloading the file")
# # downloading the file
# downloaded_file = files.get("2023-01-01T00:00", "BEBILZ_SYS001")

# print("loading files")
# # loading files
# downloaded_file.load()
# print("signal : ", (cached_file.signal.data == downloaded_file.signal.data).all())

# print("comparing files")
# # comparing files
# print("cached_file == downloaded_file :", cached_file == downloaded_file)
# print("cached_file.signal == downloaded_file.signal :", cached_file.signal == downloaded_file.signal)


# print("beacon_freq : ", cached_file.signal.beacon_frequency == downloaded_file.signal.beacon_frequency)
# print("signal : ", (cached_file.signal.data == downloaded_file.signal.data).all())
# print("samplerate : ", cached_file.signal.samplerate == downloaded_file.signal.samplerate)
# print("nfft : ", cached_file.signal.nfft == downloaded_file.signal.nfft)
# print("fft : ", (cached_file.signal.fft == downloaded_file.signal.fft).all())
# print("real_fft_freq : ", (cached_file.signal.real_fft_freq == downloaded_file.signal.real_fft_freq).all())
# print("real_fft : ", (cached_file.signal.real_fft == downloaded_file.signal.real_fft).all())

# enable_cache()

# for system_code, file in files.get("2023-10-10T00:00", ["BEBILZ_SYS001", "BEHUMA_SYS003"]).items():
    
#     file.process()
#     print(system_code, file.beacon_frequency, file.signal.data.dtype)


# systems = [
#     "BEHUMA_SYS001",
#     "BEHUMA_SYS002",
#     "BEHUMA_SYS003",
#     "BEBILZ_SYS001",
#     "FRHAGN_SYS001",
#     "NLMAAS_SYS001",
# ]

# file_cache = 0
# memory_cache = 0

# for i in range(25):

#     start = timeit.default_timer()
#     for file in files.get("2023-10-10T12:05", systems).values():
#         print("s", systems)
#         file.load()
#         cache.Cache.data = {}

#     file_cache += timeit.default_timer() - start

# for i in range(25):

#     start = timeit.default_timer()
#     for file in files.get("2023-10-10T12:05", systems).values():
#         file.load()

#     memory_cache += timeit.default_timer() - start

# print("time file cache :", file_cache)
# print("time memory cache :", memory_cache)
