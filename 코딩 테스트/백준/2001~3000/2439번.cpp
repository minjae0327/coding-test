#include <iostream>
#include <string>

int main()
{
    int n;
    std::cin >> n;

    for (int i = 1; i <= 5; i++)
    {
        for (int j = n-i; j > 0; j--)
        {
            std::cout << " ";
        }
        for (int k = 0; k < i; k++)
        {
            std::cout << "*";
        }
        std::cout<<"\n";
    }
        
    return 0;
}