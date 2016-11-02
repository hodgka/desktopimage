#ifndef __GRID_H
#define __GRID_H

#include <vector>
#include <string>
#include <unordered_map>
#include <stack>
#include <utility>
#include <functional>

#include "cell.h"

using std::vector;
using std::string;
using std::pair;

// no hash function for pair<int,int>, so wrap simple hash in struct
// and pass it to unordered_map on initialization
struct hash_pair {
    inline std::size_t operator()(const std::pair<int,int> & v) const {
        std::hash<int> int_hash;
        return int_hash(v.first)^int_hash(v.second);
    }
};

class Grid {
public:
    Grid( vector<string>& lines, int m, int n);

    int get_m() const { return _m; }
    int get_n() const { return _n; }
    Cell get_cell(int x, int y) const { return _grid[y][x]; }

    bool isNum(string& str);
    double evaluate_RPN(const vector<string>& expression);
    double evaluate(Cell& current_cell);
    vector<double> Output_Values();

private:
    vector<vector<Cell> > _grid;
    int _m, _n;
    bool _cycle;
    // would have liked to hash cells, but didn't want to design a hash for them.
    // Using hashmap instead of stack here because O(1) lookup for all elements
    std::unordered_map<pair<int, int> , bool, hash_pair> _visited_cells;
};

#endif
