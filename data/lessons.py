"""Short lesson content per subject, shown on the Lesson screen."""

LESSONS = {
    "Verbal Ability": {
        "title": "Word Power & Sentence Sense",
        "intro": "Verbal Ability tests how well you understand and use the English language — "
                  "vocabulary, grammar, analogies, and reading comprehension.",
        "points": [
            "Learn root words, prefixes, and suffixes to decode unfamiliar vocabulary quickly.",
            "Subject-verb agreement: the verb must match the TRUE subject of the sentence, not a word in between.",
            "Analogies test relationships (tool-to-user, part-to-whole, cause-to-effect) — name the relationship first.",
            "Read every choice before picking the \"best\" answer; CSE often has close distractors.",
        ],
        "example_label": "Worked Example",
        "example": "\"The board of directors ____ meeting next Monday.\" → \"is\" (board is a singular collective noun).",
        "tip": "When stuck on vocabulary, look for a familiar root word inside the unfamiliar one.",
    },
    "Numerical Ability": {
        "title": "Numbers, Ratios & Word Problems",
        "intro": "Numerical Ability covers arithmetic, percentages, ratios, averages, and "
                  "word-problem reasoning — speed and accuracy both matter.",
        "points": [
            "Convert percentages to decimals before multiplying: 15% = 0.15.",
            "For \"work\" problems, find the combined daily rate, then solve for time.",
            "Ratio problems: add the parts of the ratio first to find the value of \"one part.\"",
            "Estimate first to eliminate obviously wrong choices before calculating precisely.",
        ],
        "example_label": "Worked Example",
        "example": "15% of 240 → 0.15 × 240 = 36.",
        "tip": "Write down the formula before plugging in numbers — it prevents careless errors under time pressure.",
    },
    "Analytical Ability": {
        "title": "Logic, Patterns & Reasoning",
        "intro": "Analytical Ability measures logical reasoning — sequences, syllogisms, "
                  "odd-one-out, and deduction from given statements.",
        "points": [
            "For syllogisms, draw a quick circle diagram (Venn-style) if the wording feels confusing.",
            "Number series: check the difference between consecutive terms first, then the ratio.",
            "\"Some,\" \"all,\" and \"no\" change a syllogism's logic completely — read these qualifiers carefully.",
            "If a conclusion \"must be true\" only sometimes, the correct answer is usually \"cannot be determined.\"",
        ],
        "example_label": "Worked Example",
        "example": "2, 6, 12, 20, 30 → differences are 4, 6, 8, 10 (each +2) → next difference is 12 → 30+12 = 42.",
        "tip": "Don't overthink simple patterns — try the most obvious rule (add, multiply, alternate) first.",
    },
    "General Information": {
        "title": "Philippine Government & Civics",
        "intro": "General Information covers the Philippine Constitution, government structure, "
                  "civil service rules, and current general knowledge.",
        "points": [
            "The 1987 Constitution established three branches: Executive, Legislative, and Judiciary.",
            "Congress is bicameral — composed of the Senate and the House of Representatives.",
            "The Civil Service Commission (CSC) is the central HR agency of the Philippine government.",
            "RA 6713 governs the ethical conduct expected of all public officials and employees.",
        ],
        "example_label": "Key Fact",
        "example": "The President of the Philippines serves a single six-year term with no re-election.",
        "tip": "Connect facts to real institutions you already recognize — it makes recall far easier under exam pressure.",
    },
}
