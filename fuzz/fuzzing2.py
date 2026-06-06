import marshal
import random
import string
import hashlib
import copy


def serialize(obj):
    return marshal.dumps(obj)


def generate_valid_random_code(seed=None):
    if seed:
        random.seed(seed)

    def ran_name(prefix=""):
        length = random.randint(3, 15)
        chars = string.ascii_letters + "_"
        return (
            prefix
            + random.choice(string.ascii_lowercase)
            + "".join(random.choice(chars + string.digits)
                      for _ in range(length - 1))
        )

    def ran_int():
        return random.randint(-1000, 1000)

    def random_float():
        return random.uniform(-1000, 1000)

    def random_string():
        length = random.randint(0, 30)
        return "".join(
            random.choice(string.ascii_letters + string.digits + " ")
            for _ in range(length)
        )

    def safe_expr(depth=0):
        """Generate safe expressions with balanced parentheses"""
        if depth > 3:
            choice = random.random()
            if choice < 0.33:
                return repr(ran_int())
            elif choice < 0.66:
                return repr(random_float())
            else:
                return repr(random_string())

        expr_type = random.random()
        if expr_type < 0.4:
            choice = random.random()
            if choice < 0.33:
                return repr(ran_int())
            elif choice < 0.66:
                return repr(random_float())
            else:
                return repr(random_string())
        elif expr_type < 0.7:
            left = safe_expr(depth + 1)
            right = safe_expr(depth + 1)
            op = random.choice(["+", "-", "*", "/", "%", "and", "or"])
            return f"({left} {op} {right})"
        else:
            func = random.choice(["abs", "len", "int", "float", "str"])
            arg = safe_expr(depth + 1)
            return f"{func}({arg})"

    code_parts = []

    imports = []
    if random.random() > 0.6:
        imports.append("import sys")
    if random.random() > 0.7:
        imports.append("import math")
    if random.random() > 0.8:
        imports.append("from collections import defaultdict")
    code_parts.extend(imports)

    for _ in range(random.randint(2, 8)):
        var_name = ran_name("g_")
        val = safe_expr()
        code_parts.append(f"{var_name} = {val}")

    for _ in range(random.randint(2, 6)):
        func_name = ran_name("func_")
        param_count = random.randint(0, 4)
        params = [ran_name("p") for _ in range(param_count)]
        params_str = ", ".join(params)

        body_lines = []
        for __ in range(random.randint(3, 12)):
            stmt = random.random()
            if stmt < 0.5:
                var = ran_name("v")
                body_lines.append(f"    {var} = {safe_expr()}")
            elif stmt < 0.8:
                condition = safe_expr()
                body_lines.append(f"    if {condition}:")
                body_lines.append(f"        {ran_name('x')} = {safe_expr()}")
                if random.random() > 0.5:
                    body_lines.append("    else:")
                    body_lines.append(
                        f"        {ran_name('y')} = {safe_expr()}")
            else:
                iter_var = ran_name("i")
                body_lines.append(
                    f"    for {iter_var} in range({ran_int() % 10}):")
                body_lines.append(f"        {ran_name('z')} = {safe_expr()}")

        if random.random() > 0.5:
            body_lines.append(f"    return {safe_expr()}")

        code_parts.append(f"def {func_name}({params_str}):")
        code_parts.extend(body_lines)

    for _ in range(random.randint(1, 4)):
        class_name = ran_name("Class")
        code_parts.append(f"class {class_name}:")

        for __ in range(random.randint(1, 4)):
            code_parts.append(f"    {ran_name('cv')} = {safe_expr()}")

        for __ in range(random.randint(1, 5)):
            method_name = ran_name("method_")
            param_count = random.randint(0, 3)
            params = [ran_name("p") for _ in range(param_count)]
            params_str = ", ".join(["self"] + params)

            method_body = []
            for ___ in range(random.randint(2, 8)):
                method_body.append(f"        {ran_name('mv')} = {safe_expr()}")

            if random.random() > 0.5:
                method_body.append(f"        return {safe_expr()}")

            code_parts.append(f"    def {method_name}({params_str}):")
            code_parts.extend(method_body)

    for _ in range(random.randint(5, 20)):
        stmt = random.random()
        if stmt < 0.6:
            code_parts.append(f"{ran_name('t')} = {safe_expr()}")
        elif stmt < 0.8:
            code_parts.append(f"if {safe_expr()}:")
            code_parts.append(f"    {ran_name('r')} = {safe_expr()}")
        else:
            func_call = (
                ran_name("func_")
                + f"({', '.join(safe_expr() for _ in
                      range(random.randint(0, 3)))})"
            )
            code_parts.append(func_call)

    return "\n".join(code_parts)


def test_code_obj_serialize_stability():
    """Test the output stability of marshal.dumps() on code objects"""

    stable_count = 0
    unstable_count = 0

    print("Starting stability test, 500 iterations...")
    print("=" * 60)

    for i in range(500):
        seed = random.randint(0, 2**31 - 1)

        try:
            code_str = generate_valid_random_code(seed)

            try:
                code_obj = compile(code_str, f"<random_code_{seed}>", "exec")
            except SyntaxError as e:
                print(f"Iteration {i+1:3d}: Syntax error (rare), skipping")
                unstable_count += 1
                continue

            serialized1 = serialize(code_obj)
            serialized2 = serialize(code_obj)
            serialized3 = serialize(copy.deepcopy(code_obj))

            hash1 = hashlib.sha256(serialized1).hexdigest()
            hash2 = hashlib.sha256(serialized2).hexdigest()
            hash3 = hashlib.sha256(serialized3).hexdigest()

            is_stable = hash1 == hash2 == hash3

            if is_stable:
                stable_count += 1
                status = " Stable"
            else:
                unstable_count += 1
                status = " Unstable"

            print(
                f"{i+1:3d}/500:{status}|Seed={seed:10d}|{hash1[:8]}..."
            )

        except Exception as e:
            print(f"Iteration {i+1:3d}/500: ✗ Exception - {str(e)[:50]}")
            unstable_count += 1

    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    print(f"Total iterations: 500")
    print(f"Stable count: {stable_count}")
    print(f"Unstable count: {unstable_count}")
    print(f"Stability ratio: {stable_count/5:.1f}%")

    if unstable_count == 0:
        print(
            "\n Conclusion: marshal.dumps() produces completely stable output "
        )
    else:
        print(
            f"\n Found {unstable_count} unstable cases"
        )


if __name__ == "__main__":
    test_code_obj_serialize_stability()
