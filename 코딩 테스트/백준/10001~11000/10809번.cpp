#include <iostream>
#include <string>

int main()
{
    std::string n;
    std::cin >> n;

    std::string alphabet = "abcdefghijklmnopqrstuvwxyz";

    for (int i = 0; i < alphabet.length(); i++)
    {
        std::cout << (int)n.find(alphabet[i]) << " ";
    }

    return 0;
}