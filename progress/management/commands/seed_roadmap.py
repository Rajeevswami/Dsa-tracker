from django.core.management.base import BaseCommand
from progress.models import Topic, Problem

ROADMAP = {
    1: {
        "title": "Arrays + Strings + Hashing",
        "problems": [
            ("Two Sum", "Hashing", "EASY"),
            ("Best Time to Buy/Sell Stock", "Sliding Window", "EASY"),
            ("Contains Duplicate", "Hashing", "EASY"),
            ("Product of Array Except Self", "Prefix/Suffix", "MEDIUM"),
            ("Maximum Subarray", "Kadane's", "MEDIUM"),
            ("Longest Substring Without Repeating Characters", "Sliding Window", "MEDIUM"),
            ("Group Anagrams", "Hashing", "MEDIUM"),
            ("Valid Anagram", "Hashing", "EASY"),
            ("Longest Consecutive Sequence", "Hashing", "MEDIUM"),
            ("3Sum", "Two Pointers", "MEDIUM"),
        ],
    },
    2: {
        "title": "Linked List + Stack/Queue",
        "problems": [
            ("Reverse Linked List", "Two Pointers", "EASY"),
            ("Merge Two Sorted Lists", "Linked List", "EASY"),
            ("Linked List Cycle", "Fast/Slow Pointers", "EASY"),
            ("Remove Nth Node From End", "Two Pointers", "MEDIUM"),
            ("Reorder List", "Linked List", "MEDIUM"),
            ("Valid Parentheses", "Stack", "EASY"),
            ("Min Stack", "Stack", "MEDIUM"),
            ("Evaluate Reverse Polish Notation", "Stack", "MEDIUM"),
            ("Daily Temperatures", "Monotonic Stack", "MEDIUM"),
            ("Implement Queue using Stacks", "Stack", "EASY"),
        ],
    },
    3: {
        "title": "Binary Search + Recursion + Sorting",
        "problems": [
            ("Binary Search", "Binary Search", "EASY"),
            ("Search in Rotated Sorted Array", "Binary Search", "MEDIUM"),
            ("Find Minimum in Rotated Sorted Array", "Binary Search", "MEDIUM"),
            ("Koko Eating Bananas", "Binary Search on Answer", "MEDIUM"),
            ("Merge Sort (from scratch)", "Sorting", "MEDIUM"),
            ("Quick Sort (from scratch)", "Sorting", "MEDIUM"),
            ("Kth Largest Element in Array", "Heap/QuickSelect", "MEDIUM"),
            ("Sort Colors", "Dutch Flag", "MEDIUM"),
        ],
    },
    4: {
        "title": "Trees (Binary Tree + BST)",
        "problems": [
            ("Invert Binary Tree", "DFS", "EASY"),
            ("Maximum Depth of Binary Tree", "DFS", "EASY"),
            ("Same Tree", "DFS", "EASY"),
            ("Level Order Traversal", "BFS", "MEDIUM"),
            ("Diameter of Binary Tree", "DFS", "EASY"),
            ("Balanced Binary Tree", "DFS", "EASY"),
            ("Lowest Common Ancestor of BST", "BST", "MEDIUM"),
            ("Validate Binary Search Tree", "BST", "MEDIUM"),
            ("Kth Smallest Element in BST", "BST", "MEDIUM"),
            ("Serialize and Deserialize Binary Tree", "DFS", "HARD"),
        ],
    },
    5: {
        "title": "Graphs",
        "problems": [
            ("Number of Islands", "BFS/DFS", "MEDIUM"),
            ("Clone Graph", "BFS/DFS", "MEDIUM"),
            ("Pacific Atlantic Water Flow", "BFS/DFS", "MEDIUM"),
            ("Course Schedule", "Topological Sort", "MEDIUM"),
            ("Rotting Oranges", "Multi-source BFS", "MEDIUM"),
            ("Word Ladder", "BFS", "HARD"),
            ("Graph Valid Tree", "Union Find", "MEDIUM"),
            ("Number of Connected Components", "Union Find", "MEDIUM"),
        ],
    },
    6: {
        "title": "Dynamic Programming (1D)",
        "problems": [
            ("Climbing Stairs", "DP", "EASY"),
            ("House Robber", "DP", "MEDIUM"),
            ("House Robber II", "DP", "MEDIUM"),
            ("Longest Palindromic Substring", "DP", "MEDIUM"),
            ("Palindromic Substrings", "DP", "MEDIUM"),
            ("Decode Ways", "DP", "MEDIUM"),
            ("Coin Change", "DP", "MEDIUM"),
            ("Maximum Product Subarray", "DP", "MEDIUM"),
            ("Word Break", "DP", "MEDIUM"),
            ("Longest Increasing Subsequence", "DP", "MEDIUM"),
        ],
    },
    7: {
        "title": "DP (2D) + Backtracking",
        "problems": [
            ("Unique Paths", "Grid DP", "MEDIUM"),
            ("Longest Common Subsequence", "Grid DP", "MEDIUM"),
            ("Edit Distance", "Grid DP", "HARD"),
            ("0/1 Knapsack", "Grid DP", "MEDIUM"),
            ("Subsets", "Backtracking", "MEDIUM"),
            ("Combination Sum", "Backtracking", "MEDIUM"),
            ("Permutations", "Backtracking", "MEDIUM"),
            ("Word Search", "Backtracking", "MEDIUM"),
            ("N-Queens", "Backtracking", "HARD"),
        ],
    },
    8: {
        "title": "Heaps + Tries + Revision",
        "problems": [
            ("Kth Largest Element in a Stream", "Heap", "EASY"),
            ("Top K Frequent Elements", "Heap", "MEDIUM"),
            ("Find Median from Data Stream", "Heap", "HARD"),
            ("Implement Trie", "Trie", "MEDIUM"),
            ("Design Add and Search Word", "Trie", "MEDIUM"),
        ],
    },
}


class Command(BaseCommand):
    help = "Seeds the database with the 8-week DSA roadmap (topics + problems)."

    def handle(self, *args, **options):
        created_topics = 0
        created_problems = 0

        for week_number, data in ROADMAP.items():
            topic, was_created = Topic.objects.get_or_create(
                week_number=week_number,
                defaults={"title": data["title"]},
            )
            created_topics += int(was_created)

            for order, (name, pattern, difficulty) in enumerate(data["problems"]):
                _obj, was_created = Problem.objects.get_or_create(
                    topic=topic,
                    name=name,
                    defaults={"pattern": pattern, "difficulty": difficulty, "order": order},
                )
                created_problems += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Topics created: {created_topics}, Problems created: {created_problems}."
            )
        )
