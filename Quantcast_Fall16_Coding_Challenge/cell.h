#ifndef __CELL_H
#define __CELL_H

#include <vector>
#include <string>
#include <utility>
#include <unordered_map>
#include <typeinfo>
#include <iostream>
#include <cstdlib>
#include <sstream>
#include <regex>

using std::vector;
using std::string;
using std::pair;

// need to use helper function from grid.cpp
// Grid also needs it, so declare extern so it won't complain about multiple definitions
extern pair<int, int> label_to_xy(const string& str);


// kinda short, so I put it all here instead of partly in a .cpp file
// in reality this really should be a templated class, but I'm lazy
class Cell{
public:
    // Constructors
    Cell() : _x(-1), _y(-1), _row(-1), _col(-1), _type("") {}
    Cell(string& data, int x, int y){
        _x = x;
        _y = y;
        add_data(data);
    }

    //MODIFIERS
    void add_data(string& data){
        // helper function to split up data into vector of strings
        _RPN = split_string(data);
        if (_RPN.size() > 1){
            _type = "expression";
            _row = -1;
            _col = -1;
            for (size_t i = 0; i < _RPN.size(); i++) {
                _children[i] = label_to_xy(_RPN[i]);
            }
        } else {
            try {
                _type = "value";
                _value =  std::stod(_RPN[0]);
                _row = -1;
                _col = -1;

            } catch (...) {
                _type = "cell";
                // Cheaper to just store the value than rerun the function
                // In theory I feel like this would work, but I don't actually know how to use tie, so...
                // _row, _col = std::tie(label_to_xy(_RPN[0]))
                pair<int, int> temp = label_to_xy(_RPN[0]);
                _row = temp.first;
                _col = temp.second;
            }
        }
    }
    void set_x(int x){_x = x; }
    void set_y(int y){ _y = y;}
    void set_type(string& t) { _type = t;}
    void set_value(double d){ _value = d;}

    //ACCESSORS
    int get_x() const { return _x; }
    int get_y() const { return _y; }
    pair<int, int> get_coords() const{
        return std::make_pair(_x, _y);
    }
    int get_child_row() const {return _row;}
    int get_child_col() const {return _col;}
    string get_type() const {return _type;}

    //vector of strings in RPN
    vector<string> get_RPN() const { return _RPN;}
    //  A double which is just values(RPN) evaluated
    double get_value() const {return _value;}

    pair<int, int> get_child(int index) { return _children[index]; }
    std::unordered_map<int,pair<int, int> > get_all_children() const{
        return _children;
    }

private:
    // row and col should just be a pointer to another cell, but
    // this is easier for now...
    int _x, _y, _row, _col;
    string _type;
    vector<string> _RPN;
    double _value;
    std::unordered_map<int,pair<int, int> > _children;

    // C++ has awful input parsing
    vector<string> split_string(string& str){
        string buffer;
        std::istringstream ss(str);
        vector<string> tokens;
        while (ss >> buffer)
            // cout<<buffer<<endl;
            tokens.push_back(buffer);
        return tokens;
    }
};

// should define a print function for cell, but compiler was complaining,
// so it will remain commented out
/*
std::ostream& operator<<(std::ostream& ostr, const Cell &c) {
    vector<string> vals = c.get_RPN();
    for (size_t i = 0; i < vals.size(); i++) {
        ostr<< vals[i];
    }
  // ostr<<c.get_RPN();
  return ostr;
}
*/


#endif
