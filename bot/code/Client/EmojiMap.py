


class EmojiMap:

    emojis = {
        # Numbers:
        ':zero:': b'0\u20e3',
        ':one:': b'1\u20e3',
        ':two:': b'2\u20e3',
        ':three:': b'3\u20e3',
        ':four:': b'4\u20e3',
        ':five:': b'5\u20e3',
        ':six:': b'6\u20e3',
        ':seven:': b'7\u20e3',
        ':eight:': b'8\u20e3',
        ':nine:': b'9\u20e3',
        ':keycap_ten:': b'\U0001f51f',

        # People
        ':family_mmbb:': b'\U0001f468\u200d\U0001f468\u200d\U0001f466\u200d\U0001f466',
        ':family_mwgb:': b'\U0001f468\u200d\U0001f469\u200d\U0001f467\u200d\U0001f466',
        ':family_wwbb:': b'\U0001f469\u200d\U0001f469\u200d\U0001f466\u200d\U0001f466',
        ':ghost:': b'\U0001f47b',
        ':robot:': b'\U0001f916',
        ':runner:': b'\U0001f3c3',


        # Symbol
        ':anger:': b'\U0001f4a2',
        ':dash:': b'\U0001f4a8',
        ':droplet:': b'\U0001f4a7',
        ':gear:': b'\u2699',
        ':globe_with_meridians:': b'\U0001f310',
        ':new:': b'\U0001f195',
        ':ocean:': b'\U0001f30a',
        ':octagonal_sign:': b'\U0001f6d1',
        ':skull_crossbones:': b'\u2620',
        ':speech_balloon:': b'\U0001f4ac',
        ':speech_left:': b'\U0001f5e8',
        ':sweat_drops:': b'\U0001f4a6',
        ':zap:': b'\u26a1',

        # Things
        ':boom:': b'\U0001f4a5',
        ':coffin:': b'\u26b0',
        ':control_knobs:': b'\U0001f39b',
        ':dagger:': b'\U0001f5e1',
        ':fishing_pole_and_fish:': b'\U0001f3a3',
        ':fist:': b'\u270a',
        ':floppy_disk:': b'\U0001f4be',
        ':map:': b'\U0001f5fa',
        ':nut_and_bolt:': b'\U0001f529',
        ':shield:': b'\U0001f6e1',
        ':tools:': b'\U0001f6e0',
        ':yen:': b'\U0001f4b4',

        # Weather
        ':cloud:': b'\u2601',
        ':cloud_lightning:': b'\U0001f329',
        ':cloud_rain:': b'\U0001f327',
        ':cloud_snow:': b'\U0001f328',
        ':cloud_snow:': b'\U0001f328',
        ':cloud_tornado:': b'\U0001f32a',
        ':partly_sunny:': b'\u26c5',
        ':snowflake:': b'\u2744',
        ':sunny:': b'\u2600',
        ':thunder_cloud_rain:': b'\u26c8',
        ':white_sun_cloud:': b'\U0001f325',
        ':white_sun_rain_cloud:': b'\U0001f326',
        ':white_sun_small_cloud:': b'\U0001f324',
        ':wind_blowing_face:': b'\U0001f32c',
    }


    def __call__(self, _input):

        return self.emojis[_input].decode('unicode-escape')
