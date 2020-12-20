import re

def GetRule(num, rules_dic):
    '''
    Returns the rule in regex form
    '''
    if all(not x.isdigit() for x in rules_dic[num]):
        return rules_dic[num].strip()
    regs = []
    for or_rule in rules_dic[num].split("|"):
        sub_regs = []
        for sub_rule in or_rule.split():
            sub_regs.append(GetRule(sub_rule, rules_dic))
        regs.append("".join(sub_regs))
    rules_dic[num] = "(" + "|".join(regs) + ")"
    return rules_dic[num]

if __name__ == "__main__":
    with open("input.txt") as f:
        raw = f.read().split("\n\n")

    rules = {}
    for rule in raw[0].split("\n"):
        rule_idx, rule_context = rule.split(":")
        rules[rule_idx] = rule_context.replace('"',"")
    regex_pattern_0 = GetRule("0",rules)[1:-1]
    if_fullmatch = lambda x: 1 if re.fullmatch(regex_pattern_0, x) else 0
    messages = raw[1].rstrip().split("\n")

    rule_0_fullmatch = sum([if_fullmatch(x) for x in messages])

    print("Part 1", rule_0_fullmatch)

    regex_pattern_42 = GetRule("42", rules)
    regex_pattern_31 = GetRule("31", rules)

    count = 0
    for message in messages:
        if re.match(regex_pattern_42, message) and \
           not re.fullmatch(regex_pattern_0, message):

            i, j = 0, 0
            temp_message = message
            while match := re.match(regex_pattern_42, temp_message):
                _, end = match.span()
                temp_message = temp_message[end:]
                i += 1

            if len(temp_message) == 0:
                # This means it doesn't contain rule 11 and thus is invalid
                continue

            while match := re.match(regex_pattern_31, temp_message):
                _, end = match.span()
                temp_message = temp_message[end:]
                j += 1

            if len(temp_message) == 0 and i>j:
                # If rule 31 in rule 11 is more than rule 42 in both rules
                # 8 and 11 it will be invalid.
                # rule 11 is 42 31 | 42 11 31. there will be more rule 42
                # than rule 31
                count += 1

    print("Part 2", rule_0_fullmatch + count)
