#include <iostream>
#include <algorithm>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <cassert>
#include <stdio.h>
#include "cell.h"
#include "grid.h"

using std::cout;
using std::endl;
using std::string;
using std::vector;



int main(int argc, char const *argv[]) {
    std::ifstream in_str(argv[1]);
    if (!in_str.good()){
        std::cerr<< "Could not open "<< argv[1] <<" to read.\n";
    }

    std::ofstream out_str(argv[2]);
    if(!out_str.good()){
        std::cerr<< "Could not open "<< argv[2] <<" to write.\n";
    }

    int n, m;
    string line;
    char temp;
    vector<string>  input_values;

    //doesn't clear '\n character' so use get
    in_str>> n >> m;
    temp = in_str.get();

    cout<<n<<", "<<m <<endl;
    while(std::getline(in_str, line, '\n')){
        input_values.push_back(line);
    }

    Grid grid = Grid(input_values, m, n);

    // evaluate grid
    for (int i = 0; i < grid.get_m(); i++) {
        for (int j = 0; j < grid.get_n(); j++) {
            Cell temp = grid.get_cell(i,j);
            grid.evaluate(temp);
        }
    }
    // get values from grid
    vector<double> output = grid.Output_Values();

    // print values
    cout <<n<<" "<<m<<endl;
    for(int i=0; i<output.size();++i){
        printf("%.5f\n", output[i] );
    }

  return 0;
}
