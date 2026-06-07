# Marshal white box test

## Sourcecode

I read code from cpython repository:<https://github.com/python/cpython>  
I copied `python3.14.4`  marshal related code in sourcecode folder and I annotate some key function of it in Chinese, leave it in `sourcecode/ChineseAnnotation folder`.

## Control Flow Graph

I draw control flow graph based on some key function.  
Due to the complexity of the calling process, I draw a overall architecture for implementing Marshall's `key methods` additionally.  
Due to the complexity of the source code, my analysis focuses on the sixth and seventh layers of the architecture. The shallower layers focus on `handling exceptions` and `data transformation`, while the deeper layers focus on `specific processing` of certain data.  
Due to the complexity of the path, I chose to calculate the `branch coverage` which is simpler.  
I count all branches manually, so there may be some mistakes. Due to the large number of branches used for handling exceptions in the source code, I additionally counted the branches without exception handling, because my goal is to find out the output different in different environment variable, instead of crashing the program which is the goal of `fuzzing`.  
All count and calculate result is left in `controlflowgraph/branch_coverage_manual_count.xlsx`.  

## Test Cases

All test cases are generated based on the branches of the code, and are not mainly aimed to trigger exceptions (as some exceptions, such as `memory exceptions`, are difficult to trigger `stably`).  
Because changing the Marshall version without changing the Python version may also be considered as changing the input (because version is one input when calling `marshal.dump` or `marshal.dumps`), so I added test cases that change the Marshall version by changing the Python version to prove them.  
My test cases reach `66%` branch coverage rate with error branches and `98%` branch coverage rate without error branches.

## additional

I used marshal.dump function, so there will be some file generated during test running. All these file all saved in `temp` folder.  
By the way, I leave my `temp` file here because `pyhon2.3` may be troublesome to install.
