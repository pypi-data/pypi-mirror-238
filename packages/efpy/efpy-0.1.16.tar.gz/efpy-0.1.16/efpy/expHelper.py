import yaml
import re
import copy
import warnings
import os


def getYamlConfName(pyFileName):
    return pyFileName.split(".")[0] + ".config.yaml";


def getSubExpId(pyFileName):
    pattern = r'^p\d+\.py$'
    if re.match(pattern, pyFileName):
        subExpId = int(pyFileName[1:-3])
    else:
        subExpId = 0;
    return subExpId;


def unpackAggrParam(param):
    pattern = r'^aggr_\d+$'
    delList = [];
    aggrParam = {};
    for strKey in param.keys():
        if re.match(pattern, strKey):
            param2 = param[strKey]
            delList.append(strKey)
            for strKey2 in param2.keys():
                aggrParam[strKey2] = param2[strKey2]
    for strKey in delList:
        del param[strKey]

    for strKey in aggrParam.keys():
        param[strKey] = aggrParam[strKey]
    return param


def dictConv(orgDict, updatedDict):
    for key1 in updatedDict:
        val = updatedDict[key1]
        if isinstance(val, dict):
            if not key1 in orgDict or orgDict[key1] is None:
                orgDict[key1] = {}
            dictConv(orgDict[key1], val);
        else:
            orgDict[key1] = val;


def convParam2Setting(param):
    configRes = {};
    for strKey in param.keys():
        val = param[strKey]
        keys = strKey.split('__');
        config = configRes
        for i in range(len(keys) - 1):
            ks = keys[i];
            if not ks in config:
                config[ks] = {};
            config = config[ks]
        config[keys[-1]] = val
    return configRes;

def _buildRefAllowed(config, isRef, path):
    res = True
    if isinstance(config, dict):
        for key in config:
            r1 = _buildRefAllowed(config[key], isRef, (path + '.' if path != "" else "") + key)
            res = res and r1
    elif isinstance(config, str) and config.startswith('?'):
        res = False
    isRef[path] = res
    return res

def loadSettingFromYamlSimple(backgroundYamlFile, varSettings={}):
    with open(backgroundYamlFile, 'r', encoding='utf-8') as c:
        defConfigs = list(yaml.load_all(c, Loader=yaml.FullLoader))
        theConfig = defConfigs[0]
    dictConv(theConfig, varSettings)
    return theConfig


def removeNoneSetting(param):
    rmKeys = []
    for key1 in param:
        val = param[key1]
        if val is None:
            rmKeys.append(key1)
        elif isinstance(val, dict):
            removeNoneSetting(val);
    for key1 in rmKeys:
        del param[key1]

######################################################################

def _processTree(config, isProssed, path):
    res = True
    if isinstance(config, dict):
        if '$' in config:
            res = False
            isProssed[path] = res
            return res;
        for key in config:
            r1 = _processTree(config[key], isProssed, (path + '.' if path != "" else "") + key)
            res = res and r1
    elif isinstance(config, str) and config.startswith('?'):
        res = False
    isProssed[path] = res
    return res

def _optionParse(config, orgConfig, path):
    nSuc = 0
    nFail = 0
    if isinstance(config, dict):
        if '$' in config:
            if config['$'].startswith('?'):
                refPath = config['$'][1:]
                keys = refPath.split('.');
                tmpConfig = orgConfig
                for ks in keys:
                    if '$' in tmpConfig:
                        nFail = 1
                        return (config, nSuc, nFail)
                    if ks in tmpConfig:
                        tmpConfig = tmpConfig[ks]
                    else:
                        raise SyntaxError(f'{path}的选项所引用的路径{refPath}错误')
            else:
                refPath = '<local>'
                tmpConfig = config['$']
            if not isinstance(tmpConfig, str):
                nFail = 1
                raise SyntaxError(f'配置路径{path}的关键词{tmpConfig}类型错误，为"{type(tmpConfig)}"！其类型应为str。')
                return (config, nSuc, nFail)
            if tmpConfig.startswith('?'):
                nFail = 1
                return (config, nSuc, nFail)

            if tmpConfig in config:
                nSuc = 1
                # print(f'\t成功解析{path}下的选项"?{refPath}"，所匹配的关键词为{tmpConfig}')
                return (config[tmpConfig], nSuc, nFail)
            else:
                for key in config:
                    if re.match(key, tmpConfig):
                        warnings.warn(f"配置路径{path}不存在关键词{tmpConfig}，但通过正则表达式匹配到关键词{key}！")
                        nSuc = 1
                        # print(f'\t成功解析{path}下的选项"?{refPath}"，所匹配的关键词为{tmpConfig}')
                        return (config[key], nSuc, nFail)
                if 'default' in config:
                    warnings.warn(f"配置路径{path}不存在关键词{tmpConfig}，但使用了default标签的内容！")
                    nSuc = 1
                    # print(f'\t成功解析{path}下的选项"?{refPath}"，所匹配的关键词为{tmpConfig}')
                    return (config['default'], nSuc, nFail)
                raise SyntaxError(f'配置路径{path}不存在关键词{tmpConfig}，请检查{refPath}的值！')
        else:
            for key in config:
                (res, nSuc0, nFail0) = _optionParse(config[key], orgConfig, (path + '.' if path != "" else "") + key)
                config[key] = res
                nSuc += nSuc0
                nFail += nFail0
    return (config, nSuc, nFail)


def _configRefParse(config, orgConfig, path, isProssed):
    nSuc = 0
    nFail = 0
    if isinstance(config, str) and config.startswith('?'):
        refPath = config[1:]
        if refPath in isProssed:
            if (refPath in isProssed) and isProssed[refPath]:
                keys = refPath.split('.');
                tmpConfig = orgConfig
                xx=True;
                for ks in keys:
                    if '$' in tmpConfig:
                        xx=False;
                        break;
                    tmpConfig = tmpConfig[ks]
                if xx:
                    nSuc += 1
                    # print(f'\t成功解析{path}下的引用"?{refPath}"')
                    config = tmpConfig;
                else:
                    nFail += 1
            else:
                nFail += 1
        else:
            nFail += 1
        return (config, nSuc, nFail)
    elif isinstance(config, dict):
        if '$' in config:
            return (config, nSuc, nFail)
        for key in config:
            (res, nSuc0, nFail0) = _configRefParse(config[key], orgConfig, (path + '.' if path != "" else "") + key,
                                                   isProssed)
            config[key] = res
            nSuc += nSuc0
            nFail += nFail0
    return (config, nSuc, nFail)

def confParse(config, param):
    config = copy.deepcopy(config)
    isLeftParam=True;
    isLeft2Parse = True;
    # k=1;
    isSuc=True;
    info='';
    while True:
        paramTmp = {}
        for strKey in param.keys():
            val = param[strKey]
            keys = strKey.split('__');
            configTmp = config
            xx = True;
            for i in range(len(keys) - 1):
                ks = keys[i];
                if not ks in configTmp:
                    configTmp[ks] = {};
                configTmp = configTmp[ks]
                if '$' in configTmp:
                    paramTmp[strKey] = val
                    xx = False
                    break;
            if xx:
                if '$' in configTmp:
                    paramTmp[strKey] = val
                    xx = False
                else:
                    configTmp[keys[-1]] = val
        param = paramTmp
        if len(param)==0:
            isLeftParam=False;

        isProssed = {}
        _processTree(config, isProssed, '')
        if isProssed[''] and (not isLeftParam):
            break;
        (config, nSuc1, nFail1) = _configRefParse(config, copy.deepcopy(config), '', isProssed);
        # print(f'第{k}次引用解析处理成功了{nSuc1}个，失败了{nFail1}个')
        if nSuc1 == 0 and nFail1 > 0 and (not isLeft2Parse) and (not isLeftParam):
            isSuc=False;
            info=f'存在{nFail1}个引用路径无法解析，请检查配置文件是否存在循环引用等问题！'
            break;

        (config, nSuc2, nFail2) = _optionParse(config, config, '');
        # print(f'第{k}次选项解析成功了{nSuc2}个，失败了{nFail2}个')
        if nSuc2 == 0 and nFail2 == 0:
            isLeft2Parse=False;
        if nSuc1 == 0 and nFail1 > 0 and nSuc2 == 0 and nFail2 > 0:
            isSuc=False;
            info=f'引用与选项冲突！存在{nFail1}个引用路径与{nFail2}个选项引用无法解析，请检查配置文件是否存在循环引用等问题！'
            break;
        # k+=1
    return (config,isSuc,info);

def loadSettingFromYaml(backgroundYamlFile, dynamicYamlFile, activeBackgroundYamlId=0, activeDynamicYamlId=0,
                        param={}, isOptionParse=False):
    theConfig= {};
    dyConfig= {};
    if os.path.exists(backgroundYamlFile):
        with open(backgroundYamlFile, 'r', encoding='utf-8') as c:
            defConfigs = list(yaml.load_all(c, Loader=yaml.FullLoader))
            theConfig = defConfigs[activeBackgroundYamlId]
    if os.path.exists(dynamicYamlFile):
        with open(dynamicYamlFile, 'r', encoding='utf-8') as c:
            dyConfig = list(yaml.load_all(c, Loader=yaml.FullLoader))
        if activeDynamicYamlId < 0 or activeDynamicYamlId >= len(dyConfig):
            raise RuntimeError(
                f'activeBackgroundYamlId的范围错误，activeBackgroundYamlId = {activeDynamicYamlId}, 应该在[0, {len(dyConfig)}) 内')
            return None;
        dyConfig = dyConfig[activeDynamicYamlId]
    dictConv(theConfig, dyConfig)
    if isOptionParse:
        (theConfig,isSuc,info) = confParse(theConfig, param)
        if not isSuc:
            ssErr='\n处理后出错的配置如下：\n'
            for key in theConfig:
                sErr=str({key: theConfig[key]})+'\n';
                sErr=sErr.replace("'?","'▶ ?")
                sErr=sErr.replace('"?','"▶ ?')
                ssErr+=sErr
            raise SyntaxError(info+ssErr)
    else:
        varSettings = convParam2Setting(param)
        dictConv(theConfig, varSettings)
    return theConfig