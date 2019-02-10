
    parent_instance = getattr(function, "__self__", None)
    #print(type(function))
    #print(dir(function))
    
    if parent_instance is None:
        parent_class = globals()[function.__qualname__.rstrip(f".{function.__name__}")]
    elif type(parent_instance) is type:
        parent_class = parent_instance
    else:
        parent_class = parent_instance.__class__
    print(parent_class)
    
    cache_name = f"{function.__name__}_cache"
    setattr(parent_class, cache_name, BidirectionalDict)
    