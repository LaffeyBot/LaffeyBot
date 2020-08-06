from nonebot import on_command, CommandSession
from .data_source import get_weather_of_city, get_report
from .international_city_weather import get_detail_city_weather_report
import config


@on_command('weather', aliases=('天气', '当前天气'), only_to_me=False)
async def weather(session: CommandSession):
    city = session.get('city', prompt='喵？指挥官要查询哪座城市喵？')
    weather_situation = await get_weather_of_city(city)
    await session.send(weather_situation)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


@on_command('weather_report', aliases=('天气预报',), only_to_me=False)
async def weather_report(session: CommandSession):
    city = session.get('city', prompt='喵？指挥官要查询哪座城市喵？')
    # reports = await get_report(city)
    reports = get_detail_city_weather_report(city)
    await session.send(reports)
