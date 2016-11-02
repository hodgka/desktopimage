#include <cassert>
#include <climits>
#include "grid.h"


using std::vector;
using std::string;
using std::pair;

Grid::Grid(vector<string>& values, int m, int n){
    assert(m>0 && n>0);
    _grid = vector<vector<Cell> >(n, std::vector<Cell>(m,Cell()));

    _m = m;
    _n = n;
    _cycle = false;
    int y = 0;
    int x = 0;
    for (size_t i = 0; i < values.size(); i++) {
        if ((i)%m == 0 and i != 0) {
            y++;
        }
        x = (i)/n;
        // memory errors for days
        _grid[y][x] = Cell(values[i], x, y);
    }
}

// checks if a string is a number
bool Grid::isNum(string& str){
    assert(str.size() > 0);
    char* c;
    strtol(str.c_str(), &c, 10);
    return *c == 0;
}

// evalute a vector of strings in reverse polish notation
double Grid::evaluate_RPN(const vector<string>& expression){
    assert(expression.size() > 0);

    std::stack<int> char_stack;
    for (size_t i = 0; i < expression.size(); i++) {
        string expr = expression[i];
        if (expr == "+" || expr == "-" || expr == "*" || expr == "/") {
            int n2 = char_stack.top();
            char_stack.pop();
            int n1 = char_stack.top();
            char_stack.pop();

            switch (expr[0]) {
                case '+' : { char_stack.push(n1 + n2); break; }
                case '-' : { char_stack.push(n1 - n2); break; }
                case '*' : { char_stack.push(n1 * n2); break; }
                case '/' : { char_stack.push(n1 / n2); break; }
            }
        } else {
            char_stack.push(std::atof(expr.c_str()));
        }
    }
    return char_stack.top();
};


// recursive function to evaluate each cell in the grid and find its value
double Grid::evaluate(Cell& current_cell){
    // Base Case
    if(current_cell.get_type() == "value"){
        return current_cell.get_value();
    }
    // Recurse on cell
    if (current_cell.get_type() == "cell"){
        pair<int,int> coords = current_cell.get_coords();
        std::unordered_map<pair<int,int>, bool, hash_pair>::const_iterator
            itr = _visited_cells.find(coords);
        // has a cycle
        if (itr != _visited_cells.end()){
            return INT_MAX;
        }
        _visited_cells[coords] = true;


        current_cell.set_value(evaluate(_grid[coords.first][coords.second]));
        // remove current cell from "stack"
        _visited_cells.erase(coords);
        return current_cell.get_value();
    }

    // recurse on expression
    if (current_cell.get_type() == "expression"){
        pair<int,int> coords = current_cell.get_coords();
        std::unordered_map<pair<int,int>, bool, hash_pair>::const_iterator
            itr =_visited_cells.find(coords);
        // has a cycle
        if (itr != _visited_cells.end()){
            return INT_MAX;
        }
        _visited_cells[coords] = true;


        // evaluate each cell in the expression
        vector<string> temp;
        vector<string> values = current_cell.get_RPN();
        for (size_t i = 0; i < current_cell.get_RPN().size(); i++) {
            pair<int,int> val_coords = current_cell.get_coords();
            if ( values[i][0] == '+'|| values[i][0] == '-'|| values[i][0] == '/'|| values[i][0] == '*' ){
                continue;
            } else{
                values[i] = evaluate(_grid[val_coords.first][val_coords.second]);
            }
        }
        // update current cell's value
        current_cell.set_value(evaluate_RPN(values));
        // remove from "stack"
        _visited_cells.erase(coords);
        return current_cell.get_value();
    }
}

// Output the value of each cell in the grid
vector<double> Grid::Output_Values(){
    vector<double> values;
    for(size_t i=0;i<_grid.size();++i){
        for(size_t j=0;j<_grid[0].size();++j){
            // should be raising an exception here
            values.push_back(_grid[i][j].get_value());
        }
    }
    return values;
}

// helper function used in both grid and cell to convert coordinate to position in grid
// i.e. "A1" -> (0, 0), "B10" -> (1,9), etc
pair<int, int> label_to_xy(const std::string& str) {
    std::unordered_map<char, int> ALPHABET =
        {{'A',0},{'B',1},{'C',2},{'D',3},{'E',4},{'F',5},{'G',6},{'H',7},
        {'I',8},{'J',9},{'K',10},{'L',11},{'M',12},{'N',13},{'O',14},
        {'P',15},{'Q',16},{'R',17},{'S',18},{'T',19},{'U',20},{'V',21},
        {'W',22},{'X',23},{'Y',24},{'Z',25}};

    // check if first digit is a letter, and rest are numbers
    string pattern = "[A-Z]{1}[0-9]*";
    std::regex reg(pattern);
    if (std::regex_match (str, reg)){
        return std::make_pair( ALPHABET[str[0]],
                              std::stoi(str.substr(1)) -1);
    }
    return std::make_pair(-1, -1);
}
