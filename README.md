# **Lumen: A Sustainability-Focused Programming Language**

Lumen is a programming language designed to help developers write energy-efficient and eco-friendly code, promoting sustainability, resource optimization, and environmental impact reduction.

---

## **Purpose**
Lumen is tailored to:
- Enhance **energy efficiency** in code.
- Foster **resource optimization**.
- Raise **environmental impact awareness** among developers.

---

## **Target Domain**
Lumen is ideal for:
- **Cloud computing**
- **Large-scale data processing**
- **Artificial Intelligence (AI)**
- **Machine Learning (ML)**
- **Resource-intensive systems**

---

## **Problems Solved**
- **Energy Overhead**: Minimize unnecessary power consumption.
- **Resource Optimization**: Optimize allocation and usage of system resources.
- **Carbon Footprint Awareness**: Provide developers insights into their code’s sustainability.

---

## **Key Features**

### **CPU Functions**
- `CPU.info()`
  Returns all information about the CPU.
- `CPU.name()`
  Returns the CPU name.
- `CPU.count()`
  Returns the number of logical cores.
- `CPU.phys_cores()`
  Returns the number of physical cores.
- `CPU.freq()`
  Returns the current CPU frequency in MHz.
- `CPU.usage()`
  Returns the CPU usage percentage.
- `CPU.usage_per_core()`
  Returns the CPU usage percentage per core.

---

### **Memory Functions**
- `MEMORY.info()`
  Returns all information about memory.
- `MEMORY.total()`
  Returns total memory in GB.
- `MEMORY.available()`
  Returns available memory in GB.
- `MEMORY.usage()`
  Returns the memory used percentage.

---

### **Network Functions**
- `NETWORK.info()`
  Returns all information about the network.
- `NETWORK.sent()`
  Returns the amount of data being sent on the network in MB.
- `NETWORK.recv()`
  Returns the amount of data being received on the network in MB.
- `NETWORK.live()`
  Runs a program to display live upload and download speed.

---

### **GPU Functions**
- `GPU.info(optional=index)`
  Returns an array of GPU information.
- `GPU.name(optional=index)`
  Returns an array of GPU names.
- `GPU.usage(optional=index)`
  Returns an array of GPU memory usage percentages.
- `GPU.total(optional=index)`
  Returns an array of GPUs' total memory in GB.
- `GPU.temp(optional=index)`
  Returns an array of GPU temperatures.
  - *`optional=x`* specifies the index of the GPU.

---

### **Utility Functions**
- `len(array)`
  Returns the length of an array.
- `array.ecoSort()`
  Sorts an array using a method optimized for its size.
- `plotUsage()`
  Displays a bar graph of CPU, memory, and network usage.
- `QUIT`
  Ends the program.

---

### **Parallel Processing**
- `parallel{ urls, ... }`
  Executes tasks in parallel for optimized performance.

---

## **Getting Started**
To begin using Lumen, ensure you have the required environment set up, and import the necessary libraries for CPU, memory, network, and GPU monitoring.
