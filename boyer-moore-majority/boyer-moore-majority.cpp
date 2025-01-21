#include <iostream>
#include <vector>

// Boyer Moore's Majority Vote algorithm written in C++
// Returns the majority element if there is one
int boyerMoore(std::vector<int>& nums) {
    int n = nums.size(), target = nums.size()/2+1;
    int count = 1, candidate = nums[0];

    for (int i = 1; i < n; i++) {           
        if (nums[i] == candidate) {
            count += 1;
        } else {
            count -= 1;
        }
        if (count == 0) {
            candidate = nums[i];
            count = 1;
        }
    }

    int cur = 0;
    for (int i = 0; i < n; i++) {
        if (nums[i] == candidate) {
            cur += 1;
        }
        if (cur == target) {
            return candidate;
        }
    }

    return -1;
}


int main() {
    std::vector<int> input = {1, 1, 2, 1, 2};
    int ans = boyerMoore(input);
    std::cout << ans << std::endl;

    return 0;
}