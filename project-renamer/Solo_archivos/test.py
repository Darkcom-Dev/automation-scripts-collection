import re

def camel_to_kebab(name): 
    # Buscar las transiciones de camelCase y separarlas con un guion
    kebab_case_name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    return kebab_case_name

if __name__ == '__main__':
    print(camel_to_kebab('camel_Case_File.txt'))