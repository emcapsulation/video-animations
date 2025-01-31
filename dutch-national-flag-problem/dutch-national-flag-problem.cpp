class Solution {
public:
    void sortColors(vector<int>& nums) {
        int low = 0, mid = 0, high = nums.size()-1;
        int middle = 1;

        while (mid <= high) {
            if (nums[mid] == middle) {
                mid += 1;

            } else if (nums[mid] > middle) {
                std::swap(nums[mid], nums[high]);

                high -= 1;

            } else if (nums[mid] < middle) {
                std::swap(nums[low], nums[mid]);

                low += 1;
                mid += 1;
            }
        }
    }
};