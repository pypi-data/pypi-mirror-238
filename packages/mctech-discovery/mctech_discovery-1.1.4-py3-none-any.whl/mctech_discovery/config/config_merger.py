import re
from typing import Dict, Any, List
import functools
from log4py import logging
from .config_value import as_crypto_value, as_password_value

log = logging.getLogger('python.lib.configure.merge')
CRYPTO_CONST = '{crypto}'


ARRAY_INDEX_PATTERN = re.compile("\\[\\d+\\]$")
INTERNAL_PARAM_PATTERN = re.compile("\\$\\(([.\\w-]+)(#(\\w+))??\\)")


def config_merge(target: Dict[str, Any], source: Dict[str, Any], type: str):
    '''
    添加配置项，每一个同名的配置项都对应着一个数组，每一个数组成员的type都不同，来自不同的配置源
    :param key 配置项的key
    :param value 配置项的值
    :param type 配置项的类型，表示来自哪一种数据源
    '''
    for name, src_value in source.items():
        if src_value is None:
            continue

        index = None
        if ARRAY_INDEX_PATTERN.search(name):
            # 形如下面格式的数组
            # a.b.c[0]: 123
            # a.b.c[1]: 456
            start = name.rindex('[')
            index = name[start + 1:-1]
            index = int(index)
            name = name[0:start]

        target_value = target.get(name)

        if isinstance(index, int):
            # 合并数组中的一项
            # 处理形如下面的配置格式
            #    a.b.c[0]: 'value'
            # 此时取到的name = 'c', index = 0, value = 'value'
            # 找到targe中数组配置的值的对象
            if target_value is None:
                target_value = TypedList()
                target_value.item_type = 'array'
                target[name] = target_value

            _merge_plain_array(target_value, src_value, type, index)
        else:
            if isinstance(src_value, Dict):
                # 最终生成的json对象中非叶子节点都是object类型，不用数组表示
                # 叶子节点每个值都是数组，表示从各个配置源得到的值，最终使用的是索引为0的值
                # 非叶子节点
                if target_value is None:
                    target_value: Dict[str, Any] = {}
                    target[name] = target_value
                elif not isinstance(target_value, Dict):
                    error_msg = "配置段类型不匹配. source:%s, target:%s" % (
                        src_value, target_value)
                    raise RuntimeError(error_msg)
                config_merge(target_value, src_value, type)
            else:
                # 叶子节点或json格式的数组对象
                src_type = 'array' if isinstance(src_value, List) else 'simple'
                if target_value is None:
                    target_value = TypedList()
                    target[name] = target_value
                    target_value.item_type = src_type
                try:
                    target_type = target_value.item_type
                    if target_type != src_type:
                        error_msg = "合并的类型不一致, name: %s, sourceType: %s, sourceType: %s" % ( # noqa
                            name, target_type, src_type)
                        raise RuntimeError(error_msg)

                    # 插入到最前面
                    target_value.insert(0, {
                        'type': type,
                        'value': src_value
                    })
                except Exception:
                    log.error(
                        "合并配置时发生错误：targetValue: %s, source=%s, target=%s" % (
                            target_value, source, target)
                    )
                    raise


def _merge_plain_array(target_value, source_value, type: str, index: int):
    '''
    :param targetValue
    :param sourceValue
    :param type 配置所属的类型
    :param index
    '''
    array_value = None
    # 找到type 相同的项
    for config_item in target_value:
        if config_item["type"] == type:
            array_value = config_item.get("value")

    if array_value is None:
        array_value = TypedList()
        target_value.insert(0, {
            'type': type,
            'value': array_value
        })

    if len(array_value) != index:
        raise RuntimeError('合并数组配置必须按下标顺序合并，当前数组长度为%d，要合并的下标为%d' %
                           (len(array_value), index))
    if isinstance(source_value, Dict):
        val: Dict[str, Any] = {}
        # 如果数组中每一项都是对象，递归处理，避免最终结果中出现带[0]这样的属性
        config_merge(val, source_value, type)
        array_value.append(val)
    else:
        array_value.append(source_value)


def process_source(source: Dict[str, Any], params: Dict[str, str]):
    config: Dict[str, Any] = {}
    for key in source:
        c = config
        segments = key.split('.')
        while len(segments) > 1:
            propName = segments.pop(0)
            val = c.get(propName)
            if val is None:
                val: Dict[str, Any] = {}
                c[propName] = val
            c = val

        val = source.get(key)
        c[segments[0]] = val if not isinstance(
            val, str) else _resolve_internal_variable(val, params)
    return config


def _resolve_internal_variable(content: str, params: Dict[str, str]):
    if (content == '' or content is None):
        return content

    def replacement_fn(args):
        expr = args.group(0)
        key = args.group(1)
        param_type = args.group(3)
        if param_type is None:
            param_type = 'string'

        value = params.get(key)
        if value is None:
            raise RuntimeError("未指定变量'%s'的值" % key)

        val_type = 'string'
        if isinstance(value, bool):
            val_type = 'boolean'
        elif isinstance(value, int):
            val_type = 'number'

        if val_type != param_type and \
                (param_type != 'password' or val_type != 'string'):
            raise RuntimeError(
                "%s类型参数的传入值不正确. key: %s, type: %s" % (
                    param_type, key, val_type)
            )
        wrap = value
        if (val_type == 'string'):
            if (value.startswith(CRYPTO_CONST)):
                input = value[CRYPTO_CONST.length:]
                wrap = as_crypto_value(input)
            wrap = as_password_value(
                wrap) if param_type == 'password' else wrap

        replements.append({'expr': expr, 'key': key, 'value': wrap})
        return str(value)

    replements = []
    result_value = INTERNAL_PARAM_PATTERN.sub(replacement_fn, content)

    # 1. content不含参数时，result_value 就是content，类型也是string
    # 2. content包含多于一个参数，只能当string类型处理
    if len(replements) == 1:
        # 等于于一个参数
        item = replements[0]
        if content == item['expr']:
            # 参数与表达式完全匹配，可以直接返回参数对应的类型
            if result_value != item['value']:
                # 一般只会出现在value类型非字符串的时候
                return item['value']

    return result_value


class TypedList(List):
    def __init__(self, *args):
        super().__init__(args)
        self.item_type: str = None


def resolve_params(target: dict, params: dict):
    if params is None:
        return
    param_refs = list()
    keys = list(params.keys())
    for key in keys:
        value = params.get(key)
        if not isinstance(value, str):
            target[key] = value
            continue
        matcher = INTERNAL_PARAM_PATTERN.search(value)
        if matcher is None:
            target[key] = value
            continue

        # 找出参数引用关系
        item = {'key': key, 'refs': list()}
        param_refs.append(item)
        while matcher is not None:
            item['refs'].append(matcher.group(1))
            matcher = INTERNAL_PARAM_PATTERN.search(value, matcher.end())

    def cmp(a, b):
        if b['key'] in a['refs']:
            return 1
        if a['key'] in b['refs']:
            return -1
        return 0

    param_refs.sort(key=functools.cmp_to_key(cmp))

    for param_ref in param_refs:
        key = param_ref['key']
        expr = params.get(key)
        value = _resolve_internal_variable(expr, target)
        target[key] = value
