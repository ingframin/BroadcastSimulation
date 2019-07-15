#include<iostream>
#include<fstream>
#include<iterator>
#include<vector>
#include<string>
using namespace std;




vector<char> read_file(const char* filename){
    ifstream input_file;
    streampos fbegin,fend;
    unsigned int flength;
    input_file.open(filename);
    fbegin = input_file.tellg();
    input_file.seekg (0, ios::end);
    fend = input_file.tellg();
    flength = fend-fbegin;
    vector<char> result(flength);
    
    input_file.seekg(0,ios::beg);
    input_file.read(&result[0],flength);
    input_file.close();
        
    return result;
}

vector<unsigned char> getBitstream(vector<char>& raw){
    vector<unsigned char> bitstream;
    unsigned char buffer=0;
    int counter = 7;
    for(int i=0;i<raw.size();i++){
        if(raw[i] == 'B'){
            buffer += (1<<counter);
        }
        else{
            buffer += (0<<counter);
        }
        counter--;
        if(counter < 0){
            counter = 7;
            bitstream.push_back(buffer);
            buffer = 0;
        }
    }
    return bitstream;

}
int main(int argc, char* argv[]){
    unsigned int length;
    for(int i =0;i<20;i++){
        string s = "r1-d"+to_string(i)+"-result.txt";
        auto memblock = read_file(s.c_str());

        length = memblock.size();
        cout << "size is: " << length << " bytes.\n";

        vector<unsigned char> result = getBitstream(memblock);
    
        ofstream out_file;
        out_file.open("r1-d"+to_string(i)+".bin", ios::out | ios::app | ios::binary);
        for(auto b:result){
            out_file<<b;
        }
        out_file.close();
    }
    
    
    return 0;
}