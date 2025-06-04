#include <iostream>
#include <string>

int main()
{
    int a, b, c;
    std::cin >> a >> b >> c;

    int result1 = a + b - c;

    std::string num = std::to_string(a) + std::to_string(b);
    int result2 = std::stoi(num) - c;

    std::cout << result1 << "\n" << result2;
        
    return 0;
}