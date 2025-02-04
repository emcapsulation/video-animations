class Solution {
    public:
    int majorityElement(vector<int>& nums) {
        int n = nums.size(), target = n/2+1;
        int count = 1, candidate = nums[0];

        for (int i = 1; i < n; i++) {
            if (nums[i] == candidate) {
                count += 1;
            } else {
                count -= 1;
            }

            // Count has reached 0
            if (count == 0) {
                // Make the current element the new candidate
                candidate = nums[i];

                // Reset the count to 1
                count = 1;
            }
        }

        return candidate;
    }
};