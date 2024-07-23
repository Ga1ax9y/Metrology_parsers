import re
import pandas as pd
from matplotlib import pyplot as plt
from collections import defaultdict
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
# operators_pattern = re.compile(r'\b(?:\s*\+\+\s*|\s*\+\s*|\s*-\s*|\s*\*\s*|\s*/\s*|\s*%\s*|\s*==\s*|\s*!=\s*|\s*<\s*|\s*>\s*|\s*<=\s*'
#                                r'|\s*>=\s*|\s*&&\s*|\s*\|\|\s*|\s*=\s*|\s*\+=\s*|\s*-=\s*|\s*\*=\s*|\s*/=\s*|\s*&\s*|'
#                                r'\s*\|\s*|\s*^\s*|\s*~\s*|\s*<<\s*|\s*>>\s*|\s*for\s*|\s*while\s*|\s*break\s*|'
#                                r'\s*continue\s*|\s*foreach\s*|\s*--\s*|\s*!\s*|\s*is\s*|\s*is\s*not\s*|\s*'
#                                r'\?\?)\b')
operators_pattern = (r'(\+=|-=|\*=|==|\+\+|--|&&|\|\||=|!=|>=|<=|>>|<<|{|<|>|\+|-|\*||%|&|\||\^|=|\.;|\^'
                    r'|\bin\b|\bbreak\b|\bcontinue\b|\bswitch\b'
                    r'|\bcase\b|\bdo\b|\bcout\b|\bcin\b|\bif\b|;'
                    r'|catch\b|try\b|!|\?\?)')
conditional_operators_pattern = (r'(\bif\b|\belse\b|\belse if\b|\bswitch\b|\bcase\b|\bdefault\b)')
conditional_operators = []
def count_occurrences(strings):
    occurrences = defaultdict(int)
    for string in strings:
        occurrences[string] += 1
    return dict(occurrences)


def find_operators(code):
    operators_count = list(filter(None, re.findall(operators_pattern, code)))
    return len(operators_count), operators_count
    # for line in code.split('\n'):
    #     operators_count += len(re.findall(operators_pattern, line))
    # return operators_count
def find_conditional_operators(code):
    conditional_operators_count = list(filter(None, re.findall(conditional_operators_pattern, code)))
    return conditional_operators_count
def max_nesting_level(code):
    max_depth = 0
    current_depth = 0
    switch_depth = 0
    case_depth = 0
    count_loop = 0
    in_switch = False
    eli  = 1
    prev = 'null'
    flag = False
    for line in code.split('\n'):
        stripped = line.strip()
        if (prev.startswith('if') or prev.startswith('else if')) and stripped.startswith('else if'):
            eli += 1
            #max_depth += 1
            current_depth += 1
        if stripped.startswith('if') or stripped.startswith('else if') or stripped.startswith('else'):
            prev = stripped
            current_depth += 1
            max_depth = max(max_depth, current_depth)

        elif stripped.startswith("switch"):
            in_switch = True
        elif stripped.startswith('case'):
            if in_switch:
                switch_depth += 1
                current_depth += 1
                max_depth = max(max_depth, current_depth)
        elif stripped.startswith("for") or stripped.startswith("while") or stripped.startswith("foreach"):
            current_depth += 1
            count_loop += 1
            max_depth = max(max_depth, current_depth)
        elif stripped.startswith('break'):
            if not in_switch:
                current_depth -= 1
        elif stripped == '}':
            if case_depth > 0:
                case_depth -= 1
            else:
                if current_depth > 0 and prev == 'else':
                    current_depth -= eli
                    eli = 0
                elif current_depth > 0:
                    current_depth -= 1

                if in_switch:
                    in_switch = False
                    current_depth -= switch_depth - 1
                    switch_depth = 0
    return max_depth - 1, count_loop

def parse_conditional_operators(cond_operators):
    i = 0
    while i < len(cond_operators):
        flag = False
        if cond_operators[i] == 'if':
            if flag:
                break
            j = i + 1
            while j < len(cond_operators):
                if cond_operators[j] == 'if':
                    conditional_operators.append('if')
                    i = j - 1
                    flag = True
                    break
                if cond_operators[j] == 'else':
                    conditional_operators.append("if-else")
                    i = j
                    flag = True
                    break
                if cond_operators[j] == 'else if':
                    k = j
                    while k < len(cond_operators):
                        if cond_operators[k] == 'if':
                            i = k - 1
                            flag = True
                            conditional_operators.append("if..else-if")
                            break
                        if cond_operators[k] == 'else':
                            conditional_operators.append("if..else-if..else")
                            i = k
                            flag = True
                            break
                        k += 1
                        if k == len(cond_operators):
                            flag = True
                            conditional_operators.append("if..else-if")
                            break
                    if flag:
                        break
                    i = j
                if cond_operators[i] == "case":
                    conditional_operators.append("case")
                j += 1
                i = j
            if not flag:
                conditional_operators.append("if")
        elif cond_operators[i] == "case":  #ADD SWICH CASE
            conditional_operators.append("case") #ADD DEFAULT IF NEEDED
        i += 1
    return conditional_operators

cpp_code = '''
 string name;
 std::cin>>name;
             for(int i=0;i<3;i++)
            {
                for(int j=i+1;j<5;j++)
                {
                    for(int k=j+1; k<7;k++)
                    {
                        for(int l=k+1;l<9;l++)
                        {
                            for(int f=l+1;f<10;f++)
                            {
                                while(True)
                                {
                                    if(y==5)
                                    {
                                        switch (name)
                                        {
                                            case "Bob":
                                                std::cout << "Hello, Bob";
                                                break;
                                            case "Sam":
                                                std::cout << "Hello, Sam";
                                                break;
                                            case "Tom":
                                                std::cout << "Hello, Tom";
                                                if(i == 1)
                                                {
                                                    std::cout << "\n";
                                                    if(i == 2)
                                                    {
                                                        std::cout << "\n";
                                                    }
                                                }
                                                break;
                                            default:
                                                std::cout << "Hello, nice to meet you";
                                                break;
                                        }
                                        break;
                                    }
                                }
                                if (y == 1)
                                {
                                    std::cout << "hello, world";
                                }
                                else if (y == 2)
                                {
                                    std::cout << "how are you?";
                                }
                                else if (y == 3)
                                {
                                    std::cout << "what is it?";
                                }
                                else
                                {
                                    std::cout << "goodbye");
                                }
				                y++;
                            }
                        }
                    }
                }
            }

'''

count, li = find_operators(cpp_code)
pre_conditional_operators = find_conditional_operators(cpp_code)
max_nesting, count_loop = max_nesting_level(cpp_code)
print("count loop", count_loop)

conditional_operators_ = find_conditional_operators(cpp_code)
conditional_operators_len = len(parse_conditional_operators(conditional_operators_))


data = {
    'Metrics': ['CL', 'cl', 'CLI'],
    'Values': [conditional_operators_len + count_loop,
               round((conditional_operators_len + count_loop) / (len(li) + count_loop), 3),
               max_nesting]
}
df = pd.DataFrame(data)
fig, ax = plt.subplots()
pd.set_option('max_colwidth', 30)
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
plt.show()

print(li)
########################################
window = tk.Tk()
window.geometry("800x600")
style = ttk.Style()
style.configure("Custom.Treeview.Heading", font=("Helvetica", 16, "bold"))
style.configure("Custom.Treeview.Cell", font=("Helvetica", 16))

table = ttk.Treeview(window, style="Custom.Treeview")
table["columns"] = ("Operator", "Amount")
table.heading("Operator", text="Оператор")
table.heading("Amount", text="Количество")
occurrences = count_occurrences(li)
print(len(li))
table.insert("", "end", values=('loops', count_loop))
for string, count in occurrences.items():
    table.insert("", "end", values=(string, count))

table.insert("", "end", values=("Общее количество", len(li)+count_loop))
table.insert("", "end", values=(" ", " "))
table.insert("", "end", values=("CL", conditional_operators_len + count_loop))
table.insert("", "end", values=("cl", round((conditional_operators_len + count_loop) / (len(li) + count_loop), 3)))
table.insert("", "end", values=("CLI", max_nesting))



table.pack(expand=True, fill=tk.BOTH)

# Запускаем главный цикл обработки событий
window.mainloop()
'''

occurrences = count_occurrences(conditional_operators)
for string, count in occurrences.items():
    print(f"{string}: {count}")
print(count)
'''
############################################
print(conditional_operators)
print(f"CL {conditional_operators_len}")
print(f"cl {round(conditional_operators_len / len(li), 2)}")
print(f"CLI {max_nesting}")
