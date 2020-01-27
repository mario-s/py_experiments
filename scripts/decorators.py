#function decorators are simply wrappers to existing functions. 
#In this example let's consider a function that wraps the string output of another function by p tags.
def get_text(name):
   return "lorem ipsum, {0} dolor sit amet".format(name)

def p_decorate(func):
   def func_wrapper(name):
       return "<p>{0}</p>".format(func(name))
   return func_wrapper

def strong_decorate(func):
    def func_wrapper(name):
        return "<strong>{0}</strong>".format(func(name))
    return func_wrapper

def div_decorate(func):
    def func_wrapper(name):
        return "<div>{0}</div>".format(func(name))
    return func_wrapper


my_get_text = div_decorate(p_decorate(strong_decorate(get_text)))

print(my_get_text("John"))

#this is like my_get-text =  = p_decorate(get_text)
@div_decorate
@p_decorate
@strong_decorate
def get_text2(name):
   return "lorem ipsum, {0} dolor sit amet".format(name)

print(get_text2("John"))