#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>
#include <fstream>
#include <regex>
#include <vector>
#include <list>
#include <map>
#include <set>
#include <climits>
#include <math.h>
#include "QFileDialog"


QString Pathstr;

QString allTextOperator = "";
QString allTextOperand = "";
using namespace std;

const string ops[] = {
    ";",
    ",",

    // ТИПЫ ДАННЫХ
    "int",
    "float",
    "string",
    "double",
    "long",
    "long long",
    "char",

    // ВЕТВЛЕНИЕ И ЦИКЛЫ
    "if",
    //"else",
    "switch",
    "case",
    "do",
    "while",
    "for",

    "cout",
    "endl",

    // СКОБКИ
    "(",
    "{",
    "[",

    // ДОСТУП К Ф-ЯМ
    ".",
    "->",

    // АРИФМЕТИЧЕСКИЕ
    "+",
    "-",
    "*",
    "/",
    "%",
    "=",
    "++",
    "--",
    "-=",
    "%=",
    "+=",
    "/=",
    "*=",

    // ЛОГИЧЕСКИЕ
    "<",
    ">",
    "<=",
    ">=",
    "==",

    // КЛЮЧ СЛОВА
    "break",
    "continue",
    "class",
    "struct",
    "default",
    "goto",
    "operator",
    "return"

};

set<string> operators;
map<string, int> operator_counts, operand_counts;

class redundancy_pair
{
public:
    string f, s;
    int multiplicity;

    redundancy_pair(string a, string b, int multiplicity)
    {
        this->f = a, this->s = b, this->multiplicity = multiplicity;
    }
};

vector <redundancy_pair> redundancy_pairs;

void _popualate_redundancy_pairs()
{
    for (set<string>::iterator i = operators.begin(); i != operators.end(); i++)
    {
        for (set<string>::iterator j = operators.begin(); j != operators.end(); j++)
        {
            if ((*i) != (*j))
            {
                int num_occur = 0, pos = 0;
                while ((pos = (*i).find(*j, pos)) != string::npos)
                {
                    num_occur++;
                    pos += (*j).length();
                }
                if (num_occur > 0)
                    redundancy_pairs.push_back(redundancy_pair(*j, *i, num_occur));
            }
        }
    }
}


void _popualate_operators()
{
    int size = *(&ops + 1) - ops;
    for (int i = 0; i < size; i++)
        operators.insert(ops[i]);
}

void _adjust_redundancy()
{
    for (vector<redundancy_pair>::iterator it = redundancy_pairs.begin(); it != redundancy_pairs.end(); it++)
    {
        if (operator_counts.find((*it).s) != operator_counts.end())
            operator_counts[(*it).f] = operator_counts[(*it).f] - operator_counts[(*it).s] * ((*it).multiplicity);
    }

    return;
}


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_Calculate_button_clicked()
{
    ui->textBrowserOperand->clear();
    ui->textBrowserOperator->clear();
    allTextOperand = "";
    allTextOperator = "";

    _popualate_operators();
    _popualate_redundancy_pairs();


    regex identifier_def("[A-Za-z][A-Za-z0-9]*");

    regex number_def("\\b([0-9]+)\\b");

    smatch sm;

    ifstream file(Pathstr.toStdString());
    string input;

    if (file.is_open())
    {
        while (getline(file, input))
        {
            for (set<string>::iterator op = operators.begin(); op != operators.end(); op++)
            {
                int pos = 0;
                while ((pos = input.find(*op, pos)) != string::npos)
                {
                    if (operator_counts.find(*op) == operator_counts.end())
                        operator_counts.insert({ *op, 1 });
                    else
                        operator_counts[*op]++;

                    pos += (*op).length();
                }
            }

            string::const_iterator pos(input.cbegin());
            while (regex_search(pos, input.cend(), sm, identifier_def))
            {
                if (operators.find(sm[0]) != operators.end())
                {
                    pos += sm.position() + sm.length();
                    continue;
                }

                string operand = sm[0];
                if (operand!="else"){
                if (operand_counts.find(operand) != operand_counts.end())
                    operand_counts[operand]++;
                else
                    operand_counts.insert(make_pair(operand, 1));
                }
                pos += sm.position() + sm.length();
            }

            pos = input.cbegin();
            while (regex_search(pos, input.cend(), sm, number_def))
            {
                if (operators.find(sm[0]) != operators.end())
                {
                    pos += sm.position() + sm.length();
                    continue;
                }

                string operand = sm[0];
                if (operand_counts.find(operand) != operand_counts.end())
                    operand_counts[operand]++;
                else
                    operand_counts.insert(make_pair(operand, 1));

                pos += sm.position() + sm.length();
            }
        }

        _adjust_redundancy();
    }

    allTextOperator += "Операторы\n";
    list<string> lst;
    int N1 = 0, n1 = 0, n2 = 0, N2 = 0;
    for (map<string, int>::iterator it = operator_counts.begin(); it != operator_counts.end(); it++)
    {
        if ((*it).second) n1++;
        N1 += (*it).second;
        cout << (*it).first << "\t" << (*it).second << "\n";
        allTextOperator += QString::fromStdString((*it).first);
        allTextOperator += "\t";
        allTextOperator += QString::number((*it).second);
        allTextOperator += "\n";
    }

    allTextOperand = "Операнды\n";
    for (map<string, int>::iterator it = operand_counts.begin(); it != operand_counts.end(); it++)
    {
        if ((*it).second) n2++;
        N2 += (*it).second;
        cout << (*it).first << "\t" << (*it).second << "\n";
        allTextOperand += QString::fromStdString((*it).first);
        allTextOperand += "\t";
        allTextOperand += QString::number((*it).second);
        allTextOperand += "\n";

    }


    printf("\nn1:%d\tN1:%d\tn2:%d\tN2:%d\n", n1, N1, n2, N2);

    int size = N1 + N2;

    int vocab_size = n1 + n2;

    double volume = size * log2(vocab_size);





    QString data = "";
    cout << "n = " << vocab_size << endl;
    data+="Длина словаря(n): ";
    data+=QString::number(vocab_size);
    data+="\n";
    cout << "Длина программы: " << size << endl;
    data+="Длина программы(N): ";
    data+=QString::number(size);
    data+="\n";
    cout << "V = " << volume << endl;
    data+="Объем программы(V): ";
    data+=QString::number(volume);
    data+="\n";
    data += "Число уникальных операторов(n1): ";
    data+=QString::number(n1);
    data+="\n";
    data+="Число уникальных операндов(n2): ";
    data+=QString::number(n2);
    data+="\n";
    data+="Общее число операторов в программе(N1): ";
    data+=QString::number(N1);
    data+="\n";
    data+="Общее число операндов в программе(N2): ";
    data+=QString::number(N2);
    data+="\n";


    ui->textBrowserOperator->setText(allTextOperator);
    ui->textBrowserOperand->setText(allTextOperand);
    ui->Metrics_label->setText(data);
}


void MainWindow::on_File_button_clicked()
{
    Pathstr = QFileDialog::getOpenFileName(0, "Открыть", "", "*.txt");
}

