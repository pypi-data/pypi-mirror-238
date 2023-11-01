# 执行实验的模板
import os
import sys
from abc import abstractmethod

import efpy as tef


class ExpTemplate(object):
    '''[ExpTemplate] 实验模板类：该类提供了布置一个实验脚本的常规接口。
ExpTemplate中实验参数的定义如下：
    实验参数分为背景级参数，任务级参数以及本地参数。他们的定义如下：
        a) 背景级参数来自Yaml文件，其默认命名为bgConfig.yaml，它通常覆盖完整的参数设置。其中设置的默认参数通常是常量或者很少变动的值。
        b) 任务级参数也是来自Yaml文件，其中记录一个或一类任务的参数设置，这些参数在具体的任务中相对固定。一个任务级参数文件中可以包含多组参数设置，选择哪一组参数取决于本地参数中的pid值（默认为0，表示第一组参数）。
        c) 本地参数为dict形式，在getExpParam函数中获取。它们在实验脚本中即时设定，其中的参数往往涉及实验任务的主要变量。在同一个任务下，各个实验样例的本地参数往往也不相同。本地实验参数可以在实验环境下通过tef.getParams()获取也可以在本地环境下直接设置。
    三者的优先级顺序分别是 本地参数 > 任务级参数 > 背景级参数。优先级高的会覆盖优先级低的参数
    本地参数在分布式实验环境下由tef获取，在非分布式环境下可以直接设置。'''

    def __init__(self, workSpaceDir='', taskConfigName="taskConfig.yaml", bgConfigName="bgConfig.yaml", isShowConfig=True, isForcePrintResults=False):
        '''[ExpFramework.__init__] ExpTemplate的构造函数，创建一个ExpTemplate的子类以布置实验。
布置实验需提供以下基本参数：
    1) workSpaceDir: 工作空间路径。该路径用于存放配置文件。
    2) taskConfigName: 任务级参数的配置文件名称。
    3) bgConfig.yaml: 背景级参数的配置文件名称，默认为"bgConfig.yaml"。
    4) isShowConfig: 设置是否展示解析后的实验参数，默认为True。若为True，则打印"完整参数内容信息如下"以及"被本地参数修正的内容"。
    4) isForcePrintResults: 设置是否强制打印实验结果，默认为False。若为True，则在本地环境下依然会打印实验结果。'''
        self.workSpaceDir = workSpaceDir
        self.bgConfigName = bgConfigName
        self.taskConfigName = taskConfigName
        self.isShowConfig = isShowConfig
        self.isForcePrintResults = isForcePrintResults

    def setPakPath(self):
        '''[ExpTemplate.setPakPath] 设置包的路径。可使用类似sys.path.append或sys.path.insert等方法添加额外的路径，所添加的路径下的包将可以被import。'''
        pass

    def getExpParam(self):
        '''[ExpTemplate.getExpParam] 获取实验参数设置param。用于获取获取本地参数。默认的实验室在实验环境（tef.isExpEnv()==True）下获取本地实验参数，在本地环境（tef.isExpEnv()==False）下不设置本地实验参数。
！注意：层次性的参数不得连续包含下划线符号“_”，因为连续两个下划线符号“__”在后续会被解析为层次引用中的“.“'''
        if tef.isExpEnv():
            param = tef.getParams();
        else:
            param = {}
        return param

    @abstractmethod
    def execExp(self,theConfig):
        '''[ExpTemplate.execExp] 根据解析后的实验参数theConfig来执行实验，并返回一个dict形式表示实验结果。
参数如下：
    1) theConfig: 解析后的实验参数，dict形式。'''
        # TODO 执行实验的代码
        return None

    def modExpParam(self, param):
        '''[ExpTemplate.modExpParam] 本地参数修饰（本地参数直接可能满足某些特定的关系，这些关系可以在此处进行修饰），然后返回修饰后的参数。
参数如下：
    1) param: 待修饰的本地参数，dict形式。'''
        # TODO 本地参数修饰（本地参数直接可能满足某些特定的关系，这些关系可以在此处进行修饰）
        return param

    def expExecCond(self, param):
        '''[ExpTemplate.expExecCond] 实验执行条件是否满足，返回boolean值。若返回False，则立即停止实验，并返回空的实验结果{}。
参数如下：
    1) param: 待判断的本地参数，dict形式。'''
        return True

    def run(self):
        '''[ExpTemplate.run] 执行实验任务。
实验任务过程如下：
    1. 调用self.setPakPath()设置包的路径。
    2. 调用self.getExpParam()以获取实验参数设置param。
    3. 调用self.expExecCond(param)判断实验条件是否满足，若不满足则立即停止实验，并返回空的实验结果{}。
    4. 调用self.modExpParam(param)对实验参数进行修饰。
    5. 解析本地实验参数中的pid（默认为0），然后根据pid获取任务级参数中的第pid组参数设置。
    6. 解析param中的聚合索引。聚合索引指的是param中名称满足aggr_%d的参数。聚合索引中通常包含多个实验参数的设置，如"aggr_1":[{"dp_config__clientT":4096,"dpcr_model__args__kOrder":12},...]就表示一个实验同时设置实验参数dp_config__clientT和dpcr_model__args__kOrder。
    7. 将param值解析为层次参数结构，其中索引值内的连续下划线符号“__”会被解析为层次引用中的“.“，例如"dp_config__clientT"将被解析为"dp_config.clientT"。
    8. 按照"本地参数 > 任务级参数 > 背景级参数"的优先级顺序构建处理后的实验参数theConfig。
        处理过程支持选项解析，一个选项解析例子如下：
            alg:
            #  fedavg, fedavg, metafed, fedap, dpfed, dpAlg, dp..., 其他
              name: fldpcr
              data: mnist
              option:
                $: ?alg.name
                fedavg:
                  desc: 传统的联邦学习方法
                  data: ?alg.data
                  preData: ?alg.option.data
                metafed: 使用复制或蒸馏的阈值
                fedap: 计算的客户端权重矩阵中，对角线元素的值，即聚合过程中转移客户端模型转移自身的占比、
                dp*: 满足差分隐私的各种联邦学习方法
                default: 默认选项
        在上述例子中，alg.option的值将根据alg.name的值决定，此时alg.option称为选项参数。
        选项参数的主要特点是其包含关键词"$"，并且"$"的值通常是一个"?"开头的字符串，代表其引用的位置。这里，被引用的值要求为字符串。
        值得注意的是，被引用的值支持正则表达式匹配。如上述例子中的dp*选项，若alg.name的值与之正则匹配，则alg.option则选择该选项，例如dpcr，dpfed等算法会匹配到该选项。若连alg.name的值连正则表达式都无法匹配，则只能匹配到default（若有）选项。由此可见，选项参数的匹配过程中的优先级顺序是：
            精准匹配 > 正则表达式匹配 > default
        此外，任何带"?"开头的字符串也都表示应用，如fedavg下的data参数。并且支持链式引用，如fedavg下的data变量。
        若在引用路径中跨过了参数选项，则该引用将在选项参数被解析后再解析。因此，引用路径不应包含$，如fedavg下的preData，其引用路径alg.option.data跨过了option（选择fedavg），不应包括$或fedavg。
        该过程同时也会解析本地参数param。解析过程中本地参数会覆盖相应位置的值，不过若覆盖的路径上涉及参数选项，则优先处理参数选项。
        同时，本地参数param也支持"?"开头字符串表示的引用，这极大扩展了参数设置的能力。
    9. 移除实验参数theConfig中用于静态引用的optionRef项以及空值项。例如，若"dp_config.clientT"的值为None，则该项配置将被删除。
    10. 展示实验参数，则打印"完整参数内容信息如下"以及"被本地参数修正的内容"。是否执行该过程由isShowConfig控制。
    11. 调用self.execExp(theConfig)执行实验，并将实验结果返回至results变量并输出。'''
        # 设置包的路径
        self.setPakPath()
        # 获取实验参数设置param
        param = self.getExpParam();
        # 实验执行条件是否满足，不满足即退出程序，并在分布式实验环境输出空实验结果
        if not self.expExecCond(param):
            if self.isForcePrintResults or tef.isExpEnv():
                tef.printResult({})
            sys.exit(0)

        # 修饰实验参数设置param
        param = self.modExpParam(param)

        # 构建实验参数过程如下：
        # 得到pid，默认为0
        if 'pid' in param:
            pid = param['pid']
            del param['pid']
        else:
            pid = 0

        # 解析param中的聚合索引（格式为aggr_%d）
        # 一个聚合索引中包含多个实验参数的设置
        # 如"aggr_1":[{"dp_config__clientT":4096,"dpcr_model__args__kOrder":12},...]就表示一个实验同时设置实验参数dp_config__clientT和dpcr_model__args__kOrder
        param = tef.unpackAggrParam(param)
        # 将param值解析为层次参数结构，其中索引值内的连续下划线符号“__”会被解析为层次引用中的“.“
        varSettings = tef.convParam2Setting(param)
        # 构建实验参数
        theConfig = tef.loadSettingFromYaml(os.path.join(self.workSpaceDir, self.bgConfigName),
                                            os.path.join(self.workSpaceDir, self.taskConfigName),
                                            activeDynamicYamlId=pid, param=param, isOptionParse=True)

        # 删除用于静态引用的optionRef
        if 'optionRef' in theConfig:
            del theConfig['optionRef']
        # 移除实验参数中的空值项
        tef.removeNoneSetting(theConfig)

        # 展示实验参数
        if self.isShowConfig == True:
            print('完整参数内容信息如下：')
            for key in theConfig:
                print({key: theConfig[key]});
            if not varSettings is None and len(varSettings) > 0:
                print('其中，被本地参数修正的内容如下：')
                for key in varSettings:
                    print({key: varSettings[key]});
            else:
                print('本地参数无修正内容。')

        # 执行实验
        results = self.execExp(theConfig);

        # 输出实验结果
        if self.isForcePrintResults or tef.isExpEnv():
            tef.printResult(results)