#include <iostream>
#include <fstream>
#include <Winspool.h>

using namespace std;

int main()
{
    ofstream printer("SRP-E300");
    if (!printer)
    {
        return 1;
    }

    printer << "Test Test Test\n";
    printer << "\f";
    printer.close();
    std::cout << "Hello, World!" << std::endl;

    return 0;
}