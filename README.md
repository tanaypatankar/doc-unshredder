#  Doc-Unshredder

Reconstruct shredded document images.

## How to Run

1. **Install Requirements**  
   Make sure you have Python installed. Then install the required libraries using:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create Necessary Folders**  
   In the project root directory, create a folder named `Output`:

   ```bash
   mkdir Output
   ```

3. **Add Input Files**  
   Place all your shredded document images into the `Input` folder. The script will use these for reconstruction.

4. **Run the Script**  
   Use the following command to run the program:

   ```bash
   python main.py
   ```

## Configuration Flags
Inside main.py, you can configure the following flags:

DEBUG = 0
Set to 1 to enable debug mode

IS_TSP = 1
Set to 1 to use a Traveling Salesman Problem (TSP) algorithm
| Set to 0 for a simpler greedy heuristic algorithm.

IS_VERTICAL = 1
Set to 1 if the document strips are vertical.
| Set to 0 if the strips are horizontal.
