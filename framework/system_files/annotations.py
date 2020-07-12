from system_files.utility import stringEqualsIgnoreCase,blockPrint,enablePrint
from functools import wraps
from inspect import getcallargs
import inspect
import types

object_container = dict()
def printNothing(func_):
    printNothingEnabled = "Y"
    if(stringEqualsIgnoreCase("Y",printNothingEnabled)):
        @wraps(func_)
        def wrapper(*args, **kwargs):
            # for arg, val in getcallargs(f, *args, **kwargs).items():
            #     print(arg, val)
            blockPrint()
            return_val = func_(*args, **kwargs)
            enablePrint()
            return return_val
        return wrapper
    else:
        return func_
    
def logger(func_):
    loggerEnabled = "Y"
    if(stringEqualsIgnoreCase("Y",loggerEnabled)):
        @wraps(func_)
        def wrapper(*args, **kwargs):
            print("Entering",func_.__name__+"()")
            return_val = func_(*args, **kwargs)
            print("exiting",func_.__name__+"()")
            return return_val
        return wrapper
    else:
        return func_

def ensure_annotations(f):
    from functools import wraps
    from inspect import getcallargs
    @wraps(f)
    def wrapper(*args, **kwargs):
        for arg, val in getcallargs(f, *args, **kwargs).items():
            print(arg,val)
            if arg in f.__annotations__:
                templ = f.__annotations__[arg]
                print(templ)
                # msg = "Argument {arg} to {f} does not match annotation type {t}"
                # Check(val).is_a(templ).or_raise(EnsureError, msg.format(arg=arg, f=f, t=templ))
        return_val = f(*args, **kwargs)
        if 'return' in f.__annotations__:
            templ = f.__annotations__['return']
            msg = "Return value of {f} does not match annotation type {t}"
            # Check(return_val).is_a(templ).or_raise(EnsureError, msg.format(f=f, t=templ))
        return return_val
    return wrapper

def handleException(f_):
    handleExceptionEnabled = "Y"
    if(stringEqualsIgnoreCase("Y",handleExceptionEnabled)):
        @wraps(f_)
        def wrapper(*args, **kwargs):
            try:
                return_val = f_(*args, **kwargs)
                return return_val
            except Exception as ex:
                print(ex)
                exit(0)
        return wrapper
    else:
        return f_


def component(class_name):
    if(isClass(class_name)):
        @wraps(class_name)
        def wrapper(*args, **kwargs):
            initializeConstructor(*args, **kwargs)
            if(class_name.__name__ in object_container):
                print(class_name.__name__,"is already initialized")
                print("Object container is",object_container)
                return object_container[class_name.__name__]
            else:
                print(class_name.__name__,"is not initialized")
                print("Object container is",object_container)
                return_val = class_name(*args, **kwargs)
                object_container[class_name.__name__] = return_val
                return return_val

        def initializeConstructor(*args, **kwargs):
            print("*args",*args,"**kwargs", **kwargs)
            for parameter in list(class_name.__init__.__code__.co_varnames):
                print(parameter)
            print(str(inspect.signature(class_name.__init__)))
        return wrapper
    else:
        print("remove @singleton from",str(class_name).split(" ")[1])
        print("Your program is terminated forcefully")
        raise Exception('Error : Only class object can be singleton')

def isClass(class_name):
    if("class" in str(class_name).split(" ")[0]):
        return True
    else:
        return False

def isMethod(method_name):
    return isinstance(method_name, types.MethodType)

def isFunction(fun_name):
    return isinstance(fun_name, types.FunctionType)
    