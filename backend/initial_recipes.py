def recipes():
    return [
        {
            'name': 'Καρμπονάρα',
            'category': 'Μακαρονάδα',
            'difficulty': 2,
            'execution_time': 30,  # in minutes
            'steps': [
                {
                    'title': 'Βράσιμο Μακαρονιών',
                    'description': 'Βράζουμε τα μακαρόνια σε αλατισμένο νερό για 10 λεπτά μόλις τελειώσουν τα σουρώνουμε και προσθέτουμε λίγο λάδι',
                    'number': 1,
                    'execution_time': 10,
                    'ingredients': ['Μακαρόνια', 'Αλάτι', 'Λάδι']
                },
                {
                    'title': 'Προετοιμασία Σάλτσας',
                    'description': 'Σε ένα τηγάνι ρίχνουμε το λάδι και το κρεμμύδι και το σοτάρουμε μέχρι να μαλακώσει',
                    'number': 2,
                    'execution_time': 5,
                    'ingredients': ['Λάδι', 'Κρεμμύδι']
                },
                {
                    'title': 'Προσθήκη Μπέικον',
                    'description': 'Προσθέτουμε το μπέικον και το σοτάρουμε μέχρι να ροδίσει',
                    'number': 3,
                    'execution_time': 5,
                    'ingredients': ['Μπέικον']
                },
                {
                    'title': 'Προσθήκη Κρέμας γάλακτος',
                    'description': 'Προσθέτουμε την κρέμα γάλακτος και ανακατεύουμε',
                    'number': 4,
                    'execution_time': 5,
                    'ingredients': ['Κρέμα γάλακτος']
                },
                {
                    'title': 'Σερβίρισμα',
                    'description': 'Σερβίρουμε τα μακαρόνια σε πιάτα και προσθέτουμε την σάλτσα',
                    'number': 5,
                    'execution_time': 5,
                    'ingredients': ['Μακαρόνια', 'Σάλτσα']
                }
            ]
        },
        {
            'name': 'Σουβλάκι',
            'category': 'Κρέας',
            'difficulty': 1,
            'execution_time': 20,  # in minutes
            'steps': [
                {
                    'title': 'Προετοιμασία Σουβλακιών',
                    'description': 'Κόβουμε το κρέας σε μικρά κομμάτια και το βάζουμε στο ξύλινο σουβλάκι',
                    'number': 1,
                    'execution_time': 5,
                    'ingredients': ['Κρέας', 'Ξύλινο σουβλάκι']
                },
                {
                    'title': 'Ψήσιμο',
                    'description': 'Ψήνουμε το σουβλάκι στο κάρβουνο μέχρι να ψηθεί',
                    'number': 2,
                    'execution_time': 10,
                    'ingredients': ['Σουβλάκι', 'Κάρβουνο']
                },
                {
                    'title': 'Σερβίρισμα',
                    'description': 'Σερβίρουμε το σουβλάκι σε πιάτα με πίτα και τζατζίκι',
                    'number': 3,
                    'execution_time': 5,
                    'ingredients': ['Σουβλάκι', 'Πίτα', 'Τζατζίκι']
                }
            ]
        },
        {
            'name': 'Πίτσα α λα Καπριτσόζα',
            'category': 'Πίτσα',
            'difficulty': 3,
            'execution_time': 30,  # in minutes
            'steps': [
                {
                    'title': 'Προετοιμασία Ζύμης',
                    'description': 'Ανακατεύουμε τα υλικά της ζύμης και την αφήνουμε να φουσκώσει',
                    'number': 1,
                    'execution_time': 10,
                    'ingredients': ['Αλεύρι', 'Νερό', 'Μαγιά']
                },
                {
                    'title': 'Προετοιμασία Σάλτσας',
                    'description': 'Σε ένα τηγάνι ρίχνουμε το λάδι και το κρεμμύδι και το σοτάρουμε μέχρι να μαλακώσει',
                    'number': 2,
                    'execution_time': 5,
                    'ingredients': ['Λάδι', 'Κρεμμύδι']
                },
                {
                    'title': 'Προσθήκη Μπέικον',
                    'description': 'Προσθέτουμε το μπέικον και το σοτάρουμε μέχρι να ροδίσει',
                    'number': 3,
                    'execution_time': 5,
                    'ingredients': ['Μπέικον']
                },
                {
                    'title': 'Προσθήκη Κρέμας γάλακτος',
                    'description': 'Προσθέτουμε την κρέμα γάλακτος και ανακατεύουμε',
                    'number': 4,
                    'execution_time': 5,
                    'ingredients': ['Κρέμα γάλακτος']
                },
                {
                    'title': 'Σερβίρισμα',
                    'description': 'Σερβίρουμε τα μακαρόνια σε πιάτα και προσθέτουμε την σάλτσα',
                    'number': 5,
                    'execution_time': 5,
                    'ingredients': ['Μακαρόνια', 'Σάλτσα']
                }
            ]                
        }
    ]