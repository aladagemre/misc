#!/usr/bin/python

wire_count = 0
inside = ""
header = ""
footer = "\nendmodule"
elements = {}
class expression:
    def __init__(self, string):
        self.exp = string
    def count_parenthesis(self):
        self.left_parc = 0
        self.right_parc = 0
        for i in self.exp:
            if i == '(':
                self.left_parc += 1
            elif i == ')':
                self.right_parc += 1
        
        if self.left_parc != self.right_parc:
            print "Error! The parenthesis do not match!"
            return -1
        
        return self.left_parc, self.right_parc
        
    def inner_left_parenthesis(self):
        counter = 0
        index = 0
        for i in self.exp:
            index += 1
            
            if i == '(':
                counter += 1
                
            if counter == self.left_parc:
                return index
    
    def inner_right_parenthesis(self):
        inner_left_index = self.inner_left_parenthesis()
        index = inner_left_index
        for i in self.exp[inner_left_index : ]:
            index += 1
            if i==')':
                return index
    
    def inner_parentheses(self):
        count = self.count_parenthesis()
        if count[0] == 0:
            list = None
        elif count[0] == -1:
            list = None
        else:
            list = self.inner_left_parenthesis(), self.inner_right_parenthesis()
        return list
    
    def inner_part(self):
        if self.count_parenthesis()[0]  != 0:
            inner_left_index = self.inner_left_parenthesis()
            inner_right_index = self.inner_right_parenthesis()
            text = self.exp[inner_left_index-1 : inner_right_index] #with parenthesis
            return text, text[1:-1].strip() #(..) , ..
        else:
            return self.exp
    
    def replace_inner_with(self, new):
        old = self.inner_part()[0]
        self.exp = self.exp.replace(old,new)
        
    def info(self):
        print "/-------------------------------------\\\n"
        print "Expression: ",self.exp
        print "Paranthesis Count: ", self.count_parenthesis()
        print "Inner Parentheses Indices: ", self.inner_parentheses()
        print "Inner Part: ", self.inner_part()
        print "\\-------------------------------------/\n"
    

        
def code(exp):
    global wire_count
    global elements
    global inside
    if elements.has_key(exp): #is that exp solved before?
        wire_str = elements[exp] #if so, use the wX value.
    else:
        wire_str = "w%s" % str(wire_count) #Else use the next counter
        wire_count+=1
    #print "Exp that passes to code function = %s" % exp
    list = exp.split(" ") 
    
    list_index = 0
    for i in list:
        Apindex = i.find("'")
        if Apindex != -1: #If there is an ' character in the list element i,
            if elements.has_key(i): #Look! Is there such element in elements?
                list[index] = elements[i] #If so, change the list element to the appropriate element.
            else: #If the X' element does not exist, we should invert it!
                pass #In fact, it's not urgent! The folks can use (A not) expression.
                
        list_index+=1 #increase the i counter.
    result =  "%s(%s" % (list[1], wire_str) #or(w0
    k=0
    for i in list: #Add the even indiced elements as parameters into the result.
        if k == 0:
            result += ", %s" % str(i)
            k=1
        else:
            k=0
    
    result+=")"     #result = %s(%s, %s, %s)" % (list[1], wire_str, list[0], list[2])
    inside += result
    inside+="\n"
    
    elements[exp] = wire_str # "x1 xor x2" => "w0"
    return wire_str,result
def unique(s):
    """Return a list of the elements in s, but without duplicates.
    """

    n = len(s)
    if n == 0:
        return []

    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u



def main():
    global header,footer,inside,wire_count
    print "Enter the expression:"
    print "For example: F = x1 xor (x2 xor x3). Leave blank for default expression."
    exp = raw_input()
    
    if exp.__len__()<2:
        exp = "F = (( ( (x1 or x2) and x3 ) xor x4 xor (x5 not) ) and (x1 or x2))"
        print "Expression is assumed as F = (( ( (x1 or x2) and x3 ) xor x4 xor (x5 not) ) and (x1 or x2))"
    
    print "Enter the module name:"
    module_name = raw_input()
    if module_name.__len__()<2:
        module_name = "figure1"
        print "Module name is assumed to be figure1"
    a = expression(exp)
    while a.count_parenthesis()[0]!=0:
        a.replace_inner_with(code(str(a.inner_part()[1]))[0])
    inputs = unique(exp.replace("(","( ").replace(")"," )").split(" "))
    equalsign = exp.find("=")
    output = exp[0:equalsign-1]
    special = [")","(","=","or","and","xor","not","nand","nor"," ","",output]
    for i in special:
        if inputs.count(i)>0:
            inputs.remove(i)
        
    inputs.sort()
    #print inputs
    header += "\n\n\n//VHDL Code for "+module_name+"\nmodule "+module_name+"("
    for i in inputs:
        header+=i+","
    header+=output+");"
    header+="\ninput "
    for i in inputs[:-1]:
	header+=i+","
    header+=str(inputs[-1:][0])+";\n"
    header+="output "+output+";\n"
    header+="wire "
    for i in range(0,wire_count):
	header+="w%s," % i
    header+="w%s" % wire_count + ";\n\n"
    print header
	    




    
    print inside
    print a.inner_part()
    print footer
    #a.info()

main()
