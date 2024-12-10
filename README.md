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

GPU.info(optional=x) returns array of GPU info
GPU.name(optional=x) returns array of GPUs' names
GPU.usage(optional=x) returns array of GPUs' memory usage percentage
GPU.total(optional=x) returns array of GPUs' total memory in GBs
GPU.temp(optional=x) returns array of GPUs' temperatures
x = index of GPU

len(array) # returns length of array

array.ecoSort() # sorts array with method based on the size of the array

plotUsage() # shows a bar graph of cpu, memory and network usage

QUIT # ends the program

parallel{
  urls,
  ...
}