# What?

This is a bundle of modules to stream and receive audio, plain data, metadata or all together.

The idea is to simulate audio streaming of any protocol for test cases.

# How?

Everything needed for pure (audio) data and shoutcast/icecast is already contained in this repository.

# Examples

## Example 1 - Stream and receive data:

1. Open two terminals.
2. Start `data_streamer` and `data_receiver` with same `port`. Define `filepath` as streamer parameter.

Terminal A:
```
python3 -m data_streamer test_files/sweep_5sec.mp3 127.0.0.1 9222
```

Terminal B:
```
python3 -m data_receiver 127.0.0.1 9222
```
