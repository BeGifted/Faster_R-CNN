import lxml.etree as etree
import torch

def parse_xml_to_dict(xml):
    """
    将xml文件解析成字典形式，参考tensorflow的recursive_parse_xml_to_dict
    Args:
        xml: xml tree obtained by parsing XML file contents using lxml.etree

    Returns:
        Python dictionary holding XML contents.
    """

    if len(xml) == 0:  # 遍历到底层，直接返回tag对应的信息
        return {xml.tag: xml.text}

    result = {}
    for child in xml:
        child_result = parse_xml_to_dict(child)  # 递归遍历标签信息
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:  # 因为object可能有多个，所以需要放入列表里
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


if __name__ == '__main__':
    scales = ((32,), (64,), (128,), (256,), (512,))
    aspect_ratios = ((0.5, 1.0, 2.0),) * len(scales)  # 重复5遍

    scales = torch.as_tensor(scales)
    aspect_ratios = torch.as_tensor(aspect_ratios)

    h_ratios = torch.sqrt(aspect_ratios)
    w_ratios = 1.0 / h_ratios

    # [r1, r2, r3]' * [s1, s2, s3]
    # number of elements is len(ratios)*len(scales)
    ws = (w_ratios[:, None] * scales[None, :])
    hs = (h_ratios[:, None] * scales[None, :])
    print(w_ratios[:, None])  # 5, 1, 3
    print(h_ratios[:, None])  # 1, 5, 1
    print(scales[None, :])
    print(ws)
    print(hs)

    ws = (w_ratios[:, None] * scales[None, :]).view(-1)
    hs = (h_ratios[:, None] * scales[None, :]).view(-1)
    print(ws)
    print(hs)

    # a = torch.rand(3, 4)
    # print(a)
    # print(a.unbind(0))
    # print(a.unbind(1))
    # xmin, ymin, xmax, ymax = a.unbind(1)
    # print(torch.stack((xmin, ymin, xmax, ymax), dim=1))

    # box = []
    # a, b, c, d = 1, 2, 3, 4
    # box.append([a, b, c, d])
    # box.append([a, c, b, d])
    # box = torch.as_tensor(box, dtype=torch.float32)
    # print(box)
    # print(box.shape)

    # with open("./VOCdevkit/VOC2012/Annotations/2007_000027.xml") as fid:
    #     xml_str = fid.read()
    # xml = etree.fromstring(xml_str)
    # data = parse_xml_to_dict(xml)["annotation"]
    # print(xml)
    # print(data)
