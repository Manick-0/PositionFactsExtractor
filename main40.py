# [['left', 'A', 'B'], ['upper-left', 'C', 'B'], ['overlap', 'C', 'E']]
# [['left', 'A', 'B'], ['upper-left', 'C', 'B'], ['overlap', 'C', 'E']]
import ast

def invert_relation(fact):
    """ Invert a spatial relation between A and B """
    relation, A, B = fact
    inverses = {
        'left': 'right',
        'right': 'left',
        'upper-left': 'lower-right',
        'lower-right': 'upper-left',
        'lower-left': 'upper-right',
         'upper-right':'lower-left',
        'above': 'below',
        'below': 'above',
        'overlap': 'overlap'
    }
    return [inverses[relation], B, A]

def infer_spatial_relations(facts):
    """ Infer new spatial relations based on given facts """
    conclusions = []
    
    for rel1 in facts:
        for rel2 in facts:
            # Avoid self-comparison
            if rel1 != rel2:
                A1, B1 = rel1[1], rel1[2]
                A2, B2 = rel2[1], rel2[2]

                # Example: If A is upper-left of B, and B is left of C, then A is above C
                if rel1[0] == 'upper-left' and rel2[0] == 'left' and B1 == B2:
                    conclusions.append(['above', A1, A2])
                
                # If A overlaps B, and A is upper-left of C, we can infer relations
                elif rel1[0] == 'overlap' and rel2[0] == 'upper-left' and A1 == A2:
                    conclusions.append(['upper-left', B1, B2])
                    conclusions.append(['above', B1, B2])
                
                # Additional rule: If A is above B, and B is below C, infer A is above C
                elif rel1[0] == 'above' and rel2[0] == 'below' and B1 == A2:
                    conclusions.append(['above', A1, B2])

                # Rule: If A is left of B, and B is left of C, then A is left of C
                elif rel1[0] == 'left' and rel2[0] == 'left' and B1 == A2:
                    conclusions.append(['left', A1, B2])

                # NEW RULE: If A is left of B, and C is above B, infer A is left and below C
                elif rel1[0] == 'left' and rel2[0] == 'above' and B1 == B2:
                    conclusions.append(['left', A1, A2])
                    conclusions.append(['below', A1, A2])

                # Extend further with additional rules
                elif rel1[0] == 'above' and rel2[0] == 'above' and B1 == A2:
                    conclusions.append(['above', A1, B2])
                    
                elif rel1[0] == 'below' and rel2[0] == 'below' and B1 == A2:
                    conclusions.append(['below', A1, B2])
                
    return conclusions

def generate_all_facts(input_facts):
    """ Generate all new facts by inverting and inferring new spatial relations """
    all_facts = set(tuple(fact) for fact in input_facts)
    new_facts = set()

    # Invert all input relations
    for fact in input_facts:
        new_facts.add(tuple(invert_relation(fact)))

    # Infer new spatial relations
    inferred = infer_spatial_relations(input_facts)
    new_facts.update(set(tuple(fact) for fact in inferred))

    # Ensure inverses of all newly generated facts are added
    for fact in list(new_facts):
        new_facts.add(tuple(invert_relation(list(fact))))

    return list(new_facts - all_facts)

def main():
    try:
        input_str = input("Enter relations in list format: ")
        facts_list = ast.literal_eval(input_str)
        
        # Validate input format
        if not isinstance(facts_list, list) or not all(isinstance(item, list) and len(item) == 3 for item in facts_list):
            raise ValueError("Input is not in the correct format.")

        # Generate new facts based on input
        new_facts = generate_all_facts(facts_list)
        print("Generated Facts:")
        
        # Print the new facts generated
        for fact in new_facts:
            print(list(fact))

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()

