CPU.info() # returns all information about cpu
CPU.name() # returns CPU name
CPU.count() #returns number of logical cores
CPU.phys_cores() # returns the number of logical cores
CPU.freq() # returns current frequency in MHz
CPU.usage() # returns CPU usage percentage
CPU.usage_per_core() # returns usage percentage per core

MEMORY.info() # returns all informations about memory
MEMORY.total() # returns total memory in GB
MEMORY.available() # returns available memory in GBs
MEMORY.usage() # return memory used percent

NETWORK.info() # returns all information about network
NETWORK.sent() # returns amount of data being sent on the network in MBs
NETWORK.recv() # returns amound of data being received on the network MBs
NETWORK.live() # runs program to display live upload and download speed

GPU.info() returns array of GPU info
GPU.name() returns array of GPUs' names
GPU.usage() returns array of GPUs' memory usage percentage
GPU.total() returns array of GPUs' total memory in GBs
GPU.temp() returns array of GPUs' temperatures
