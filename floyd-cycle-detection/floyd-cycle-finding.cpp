/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    // Floyd's cycle finding algorithm written in C++
    // Returns NULL if there is no cycle, otherwise returns a pointer to the start of the cycle
    ListNode *detectCycle(ListNode *head) {
        // Check the head
        if (head == NULL || head->next == NULL) {
            return NULL;
        }

        ListNode *tortoise = head->next;
        ListNode *hare = head->next->next;

        // Part 1: Move the tortoise and hare until they meet again
        while (tortoise != hare) {
            // Hare has reached the end, indicating there is no cycle
            if (hare == NULL || hare->next == NULL) {
                return NULL;
            }

            // Move the tortoise one node
            tortoise = tortoise->next;

            // Move the hare two nodes
            hare = hare->next->next;
        }

        // Part 2: Move the tortoise back to the head of the LL
        tortoise = head;

        while (tortoise != hare) {
            // Step the tortoise and hare one node at a time until they meet at the entry point
            tortoise = tortoise->next;
            hare = hare->next;
        }

        // Return the entry point of the cycle
        return tortoise;
    }
};