from django import http
import dodi
import html_generators as h
import html_generators.django as hd

STYLE = '''
    html {
        font-family: sans-serif;
        background: repeating-linear-gradient(-45deg, #e4e4e4, #E4E4E3 10px, white 10px, white 20px);
        background-attachment: fixed;
    }
    img {
        border: 1px solid #bbb;
    }
'''


def static_test(source, transform, message=None):
    return (
        h.H4(transform),
        h.P(message),
        h.Div(
            h.Img(src=hd.static(source)),
            h.Img(src=dodi.static_url(source, transform)),
            style='display: flex; align-items: flex-start;',
        )
    )


def test_view(request):
    return http.HttpResponse(h.Document(
        h.Title('DODI Visual Tests'),
        h.Style(STYLE),
        h.H1('DODI Visual Tests'),

        h.H2('Cropping'),
        static_test('ace_truck_200_100.jpg', 'crop_left=50'),
        static_test('ace_truck_200_100.jpg', 'crop_right=50'),
        static_test('ace_truck_200_100.jpg', 'crop_bottom=50'),
        static_test('ace_truck_200_100.jpg', 'crop_top=50'),
        static_test('ace_truck_200_100.jpg', 'crop_left=50;crop_right=50;crop_bottom=10;crop_top=10'),

        h.H2('Resizing'),
        static_test('ace_truck_200_100.jpg', 'width=100;height=100'),
        static_test('ace_truck_200_100.jpg', 'width=100;height=100;mode=crop'),
        static_test('ace_truck_200_100.jpg', 'width=100;height=100;mode=stretch'),

        h.H3('With and W/O scale_up'),
        static_test('ace_truck_200_100.jpg', 'width=400;height=200'),
        static_test('ace_truck_200_100.jpg', 'width=500;height=200;scale_up'),
        static_test('ace_truck_200_100.jpg', 'width=400;height=500;scale_up'),
        static_test('ace_truck_200_100.jpg', 'width=200;height=200;mode=crop'),
        static_test('ace_truck_200_100.jpg', 'width=200;height=200;mode=crop;scale_up'),
        static_test('ace_truck_200_100.jpg', 'width=200;height=200;mode=stretch'),
        static_test('ace_truck_200_100.jpg', 'width=200;height=200;mode=stretch;scale_up'),

        h.H3('With and W/O match_orientation'),
        static_test('ace_truck_200_100.jpg', 'width=50;height=100'),
        static_test('ace_truck_200_100.jpg', 'width=50;height=100;match_orientation'),
        static_test('ace_truck_200_100.jpg', 'width=50;height=100;mode=crop'),
        static_test('ace_truck_200_100.jpg', 'width=50;height=100;mode=crop;match_orientation'),
        static_test('ace_truck_200_100.jpg', 'width=50;height=100;mode=stretch'),
        static_test('ace_truck_200_100.jpg', 'width=50;height=100;mode=stretch;match_orientation'),

        h.H2('Rotating'),
        static_test('ace_truck_200_100.jpg', 'rotate=90'),
        static_test('ace_truck_200_100.jpg', 'rotate=180'),
        static_test('ace_truck_200_100.jpg', 'rotate=270'),

        h.H2('Overlay'),
        h.P('Note - we use different approach for jpg and png, so need to test both!'),
        h.P('Ensure the resultant png is still semi-transparent.'),
        static_test('ace_truck_200_100.jpg', 'overlay=green,0.5'),
        static_test('sun.png', 'overlay=green,0.5'),

        h.H2('Enhancers'),
        static_test('ace_truck_200_100.jpg', 'color=0.2'),
        static_test('ace_truck_200_100.jpg', 'color=0.7'),
        static_test('ace_truck_200_100.jpg', 'contrast=0.2'),
        static_test('ace_truck_200_100.jpg', 'contrast=0.7'),
        static_test('ace_truck_200_100.jpg', 'brightness=0.2'),
        static_test('ace_truck_200_100.jpg', 'brightness=0.7'),
        static_test('ace_truck_200_100.jpg', 'color=0;contrast=0.5'),

    ))