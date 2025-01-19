int majorityElement(vector<int>& nums) {
    int count = 1;
    int candidate = nums[0];

    for (size_t i = 1; i < nums.size(); i++) {           
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

    return candidate;
}