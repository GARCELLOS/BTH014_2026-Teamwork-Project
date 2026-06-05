import unittest
import marshal
import types
import sys
import math
import time
from io import BytesIO


# --------------------- 边界值定义（手动选取极值） ---------------------
def generate_boundary_values():
    """为每种 marshal 支持的类型生成边界值列表"""
    boundary_samples = []

    # --- None, StopIteration, Ellipsis, bool ---
    boundary_samples.append(("None", None))
    boundary_samples.append(("StopIteration", StopIteration))
    boundary_samples.append(("Ellipsis", ...))
    boundary_samples.append(("bool_min", False))
    boundary_samples.append(("bool_max", True))

    # --- int ---
    boundary_samples.append(("int_0", 0))
    boundary_samples.append(("int_minus1", -1))
    boundary_samples.append(("int_1", 1))
    boundary_samples.append(("int_small_min", -2**31))
    boundary_samples.append(("int_small_max", 2**31 - 1))
    boundary_samples.append(("int_very_large", 10**100))
    boundary_samples.append(("int_very_small", -10**100))

    # --- float ---
    boundary_samples.append(("float_0", 0.0))
    boundary_samples.append(("float_neg_0", -0.0))
    boundary_samples.append(("float_eps", sys.float_info.epsilon))
    boundary_samples.append(("float_max", sys.float_info.max))
    boundary_samples.append(("float_min", sys.float_info.min))
    boundary_samples.append(("float_inf", float("inf")))
    boundary_samples.append(("float_neg_inf", float("-inf")))
    boundary_samples.append(("float_nan", float("nan")))
    boundary_samples.append(("float_max_minus", sys.float_info.max * 0.9999))
    boundary_samples.append(("float_min_plus", sys.float_info.min * 1.0001))

    # --- complex ---
    boundary_samples.append(("complex_0", 0j))
    boundary_samples.append(("complex_max", complex(sys.float_info.max, sys.float_info.max)))
    boundary_samples.append(("complex_min", complex(sys.float_info.min, sys.float_info.min)))
    boundary_samples.append(("complex_nan", complex(float("nan"), float("nan"))))

    # --- bytes ---
    boundary_samples.append(("bytes_empty", b""))
    boundary_samples.append(("bytes_one_min", b"\x00"))
    boundary_samples.append(("bytes_one_max", b"\xff"))
    boundary_samples.append(("bytes_large", bytes(range(256)) * 100))

    # --- str ---
    boundary_samples.append(("str_empty", ""))
    boundary_samples.append(("str_one", "a"))
    boundary_samples.append(("str_unicode", "🍉"))
    boundary_samples.append(("str_large", "α" * 10000))

    # --- tuple ---
    boundary_samples.append(("tuple_empty", ()))
    boundary_samples.append(("tuple_one", (42,)))
    boundary_samples.append(("tuple_nested", (1, (2, (3, (4,))))))
    boundary_samples.append(("tuple_large", tuple(range(1000))))

    # --- list ---
    boundary_samples.append(("list_empty", []))
    boundary_samples.append(("list_one", [None]))
    boundary_samples.append(("list_large", list(range(1000))))

    # --- dict ---
    boundary_samples.append(("dict_empty", {}))
    boundary_samples.append(("dict_one", {"key": 1}))
    boundary_samples.append(("dict_large", {str(i): i for i in range(1000)}))

    # --- set ---
    boundary_samples.append(("set_empty", set()))
    boundary_samples.append(("set_one", {1}))
    boundary_samples.append(("set_large", set(range(1000))))

    # --- frozenset ---
    boundary_samples.append(("frozenset_empty", frozenset()))
    boundary_samples.append(("frozenset_one", frozenset([1])))
    boundary_samples.append(("frozenset_large", frozenset(range(1000))))

    # --- code ---
    def empty_func():
        pass
    boundary_samples.append(("code_empty", empty_func.__code__))

    def complex_func(a, b, c=3, *, d=4):
        x = a + b + c + d
        return x * 2
    boundary_samples.append(("code_complex", complex_func.__code__))

    return boundary_samples


# --------------------- 辅助比较函数 (处理 NaN 等) ---------------------
def marshal_equal(orig, reco):
    if isinstance(orig, float) and math.isnan(orig):
        return isinstance(reco, float) and math.isnan(reco)
    if isinstance(orig, complex):
        has_nan = (math.isnan(orig.real) or math.isnan(orig.imag) or
                   math.isnan(reco.real) or math.isnan(reco.imag))
        if has_nan:
            return (math.isnan(orig.real) == math.isnan(reco.real) and
                    math.isnan(orig.imag) == math.isnan(reco.imag))
    # 普通对象：先用 Python 相等比较，若递归过深则回退到序列化字节比较
    try:
        return type(orig) == type(reco) and orig == reco
    except RecursionError:
        return marshal.dumps(orig) == marshal.dumps(reco)


# --------------------- 深度嵌套对象构造 ---------------------
def make_deeply_nested_tuple(depth):
    """返回嵌套深度为 depth 的元组"""
    obj = ()
    for _ in range(depth):
        obj = (obj,)
    return obj

def make_deeply_nested_frozenset(depth):
    """返回嵌套深度为 depth 的冻结集合"""
    obj = frozenset()
    for _ in range(depth):
        obj = frozenset([obj])
    return obj


class TestMarshalBoundaries(unittest.TestCase):

    LARGE_OBJECT_SIZE = 100 * 1024 * 1024  # 100 MB

    @classmethod
    def setUpClass(cls):
        cls.samples = generate_boundary_values()
        cls.max_version = marshal.version

    # ---------- 原有测试 ----------
    def test_individual_roundtrip_and_tell(self):
        """对每个格式版本和每个样本，验证往返正确性及 tell() 长度"""
        for ver in range(self.max_version, 0, -1):
            for name, obj in self.samples:
                # 跳过 marshal 版本 1 无法正确往返的代码对象
                if ver == 1 and isinstance(obj, types.CodeType):
                    continue
                with self.subTest(version=ver, sample=name):
                    data = marshal.dumps(obj, ver)
                    restored = marshal.loads(data)
                    self.assertTrue(marshal_equal(obj, restored),
                                    f"往返失败: {obj!r} != {restored!r}")

                    stream = BytesIO(data)
                    marshal.load(stream)
                    self.assertEqual(stream.tell(), len(data),
                                     f"tell() 长度 {stream.tell()} ≠ dumps 长度 {len(data)}")

    def test_concatenated_stream_boundaries(self):
        """对每个格式版本，验证紧密拼接后流式加载的边界完整性"""
        for ver in range(self.max_version, 0, -1):
            parts = []
            names = []
            objects = []
            for name, obj in self.samples:
                if ver == 1 and isinstance(obj, types.CodeType):
                    continue
                data = marshal.dumps(obj, ver)
                parts.append(data)
                names.append(name)
                objects.append(obj)

            blob = b"".join(parts)
            stream = BytesIO(blob)
            recovered = []
            boundaries = []

            while stream.tell() < len(blob):
                obj = marshal.load(stream)
                recovered.append(obj)
                boundaries.append(stream.tell())

            with self.subTest(version=ver):
                self.assertEqual(len(recovered), len(objects),
                                 f"恢复对象数量 {len(recovered)} ≠ 期望 {len(objects)}")

                for i, (orig, reco) in enumerate(zip(objects, recovered)):
                    self.assertTrue(marshal_equal(orig, reco),
                                    f"版本{ver}, 索引{i} ({names[i]}) 不匹配: {orig!r} ≠ {reco!r}")

                self.assertEqual(boundaries[-1], len(blob),
                                 "最后一个边界不等于拼接总长")

                accumulated = 0
                for i, bound in enumerate(boundaries):
                    obj_len = bound - accumulated
                    expected_len = len(parts[i])
                    self.assertEqual(obj_len, expected_len,
                                     f"版本{ver}, {names[i]} 边界错误: "
                                     f"偏移差 {obj_len} ≠ 预期 {expected_len}")
                    accumulated = bound

    def test_deeply_nested_tuple(self):
        """测试接近递归限制的嵌套元组（使用自适应比较）"""
        # 使用 982，这是之前发现的安全深度（可调整）
        DEPTH = 982
        old_limit = sys.getrecursionlimit()
        try:
            sys.setrecursionlimit(max(old_limit, DEPTH + 500))
            obj = make_deeply_nested_tuple(DEPTH)
        finally:
            sys.setrecursionlimit(old_limit)

        for ver in range(self.max_version, 0, -1):
            with self.subTest(version=ver, structure=f"deep_tuple_{DEPTH}"):
                try:
                    data = marshal.dumps(obj, ver)
                except ValueError as e:
                    # marshal 拒绝深度嵌套视为正常保护
                    print(f"  [版本 {ver}] 嵌套元组序列化被拒绝: {e}")
                    continue

                restored = marshal.loads(data)
                self.assertTrue(marshal_equal(obj, restored),
                                f"版本 {ver} 深度 {DEPTH} 元组往返失败")
                
    # def test_deeply_nested_frozenset(self):
    #     """测试接近递归限制的嵌套冻结集合"""
    #     DEPTH = 982
    #     old_limit = sys.getrecursionlimit()
    #     try:
    #         sys.setrecursionlimit(max(old_limit, DEPTH + 500))
    #         obj = make_deeply_nested_frozenset(DEPTH)
    #     finally:
    #         sys.setrecursionlimit(old_limit)

    #     for ver in range(self.max_version, 0, -1):
    #         with self.subTest(version=ver, structure=f"deep_frozenset_{DEPTH}"):
    #             try:
    #                 data = marshal.dumps(obj, ver)
    #             except ValueError as e:
    #                 print(f"  [版本 {ver}] 嵌套冻结集合被拒绝: {e}")
    #                 continue

    #             restored = marshal.loads(data)
    #             self.assertTrue(marshal_equal(obj, restored),
    #                             f"版本 {ver} 深度 {DEPTH} 冻结集合往返失败")

    def test_large_object(self):
        """测试极大 bytes 对象序列化"""
        huge_bytes = b'\x00' * self.LARGE_OBJECT_SIZE

        for ver in range(self.max_version, 0, -1):
            with self.subTest(version=ver, size_mb=self.LARGE_OBJECT_SIZE // (1024*1024)):
                start = time.time()
                try:
                    data = marshal.dumps(huge_bytes, ver)
                    elapsed = time.time() - start
                except MemoryError:
                    print(f"  [版本 {ver}] 极大对象 MemoryError，跳过。")
                    continue
                except ValueError as e:
                    print(f"  [版本 {ver}] 极大对象被拒绝: {e}")
                    continue

                self.assertGreaterEqual(len(data), self.LARGE_OBJECT_SIZE)
                restored = marshal.loads(data)
                self.assertEqual(restored, huge_bytes)
                self.assertLess(elapsed, 10.0, f"版本 {ver} 极大对象序列化过慢: {elapsed:.2f}s")

    # ---------- 新增：自动搜索递归深度边界 ----------
    def test_find_recursion_boundary(self):
        """
        对每个 marshal 格式版本，找出 == 比较不会触发 RecursionError 的最大嵌套深度。
        同时提供详细的运行日志，便于诊断卡顿位置。
        """
        print("\n" + "=" * 60)
        print("嵌套深度边界搜索（带诊断输出）")
        print("Python 版本:", sys.version)
        print("递归限制:", sys.getrecursionlimit())
        print("=" * 60)

        for ver in range(self.max_version, 0, -1):
            print(f"\n--- 版本 {ver} ---")
            for container_type in ("tuple",):
                print(f"  容器类型: {container_type}")
                # ---------- 1. 查找 marshal 可序列化的最大深度 ----------
                marshal_max = 0
                low, high = 1, 2000  # 上限 2000，远大于 marshal 的 999 限制
                print("    搜索 marshal 最大序列化深度...")
                while low <= high:
                    mid = (low + high) // 2
                    # 冻结集合深度 > 1500 时构造极慢，直接假设 marshal 拒绝，跳过
                    if container_type == "frozenset" and mid > 1500:
                        print(f"      深度 {mid} > 1500, 冻结集合构造太慢，假定 marshal 拒绝")
                        high = mid - 1
                        continue
                    print(f"      尝试深度 {mid} ...", end=" ", flush=True)
                    t0 = time.time()
                    try:
                        if container_type == "tuple":
                            obj = make_deeply_nested_tuple(mid)
                        else:
                            obj = make_deeply_nested_frozenset(mid)
                        t1 = time.time()
                        print(f"构造耗时 {t1-t0:.2f}s", end=", ")
                        _ = marshal.dumps(obj, ver)
                        t2 = time.time()
                        print(f"序列化耗时 {t2-t1:.2f}s -> OK")
                        marshal_max = mid
                        low = mid + 1
                    except ValueError as e:
                        if "too deeply nested" in str(e):
                            print("被 marshal 拒绝")
                            high = mid - 1
                        else:
                            raise
                    except RecursionError:
                        print("RecursionError (构造时)")
                        high = mid - 1
                    except MemoryError:
                        print("MemoryError, 降低上限")
                        high = mid - 1
                    except Exception as e:
                        print(f"意外异常: {e}")
                        high = mid - 1

                print(f"    marshal 最大深度 = {marshal_max}")

                if marshal_max == 0:
                    print("    无法找到有效深度，跳过 == 边界搜索")
                    with self.subTest(version=ver, container=container_type):
                        self.skipTest("无法构造任何深度的对象")
                    continue

                # ---------- 2. 在 marshal 安全范围内，查找 == 比较的安全深度 ----------
                eq_safe = 0
                low, high = 1, marshal_max
                print("    搜索 == 比较的最大安全深度...")
                while low <= high:
                    mid = (low + high) // 2
                    print(f"      深度 {mid} ...", end=" ", flush=True)
                    try:
                        # 重用构造好的对象（可缓存，这里简单实现）
                        if container_type == "tuple":
                            obj = make_deeply_nested_tuple(mid)
                        else:
                            obj = make_deeply_nested_frozenset(mid)
                        data = marshal.dumps(obj, ver)
                        restored = marshal.loads(data)
                        _ = (obj == restored)   # 直接测试 == 比较
                        print("== 成功")
                        eq_safe = mid
                        low = mid + 1
                    except RecursionError:
                        print("RecursionError (== 比较时)")
                        high = mid - 1
                    except ValueError as e:
                        # marshal 已经拒绝（理论上不会发生，因为 mid ≤ marshal_max）
                        print(f"意外被 marshal 拒绝: {e}")
                        high = mid - 1
                    except MemoryError:
                        print("MemoryError")
                        high = mid - 1
                    except Exception as e:
                        print(f"意外异常: {e}")
                        high = mid - 1

                print(f"    == 比较安全深度 = {eq_safe}  (超过则 RecursionError)")

                with self.subTest(version=ver, container=container_type):
                    self.assertGreater(eq_safe, 0,
                                    f"未找到 {container_type} 的安全比较深度")

if __name__ == "__main__":
    unittest.main()