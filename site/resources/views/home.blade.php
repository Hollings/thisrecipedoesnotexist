<head>
    <style>
        .ing p {
            margin: 0 15px;
        }

        .dir p {
            margin: 15px;
        }

        .dir, .ing {
            margin-top: 50px
        }

        .content {
            border: 1px solid #cacaca;
            margin-bottom: 50px;
        }

        .footer {
            text-align: center;
            color: #adb5bd;
            font-size: 11px;
        }

        .recent-recipes {
            font-size: 12px;
        }

        .typeahead.dropdown-menu {
            max-width: 300px;
        }

        .typeahead .dropdown-item {
            white-space: initial;
        }

        body.dark-mode {
            background-color: #111;
            color: #eee;
        }

        .dark-mode .content {
            background-color: #333 !important;
            color: #eee;
        }

        .dark-mode .list-group {
            background-color: #ccc !important;
        }

        .dark-mode .list-group a {
            background-color: #333;
            color: #eee;
            border: 1px solid #555;
            border-radius: 0;
        }

        .dark-mode .alert-light {
            background-color: #222;
            border: 0;
        }
    </style>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <link rel="shortcut icon" href="{{ asset('favicon.ico') }}">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-3-typeahead/4.0.2/bootstrap3-typeahead.min.js"></script>

    @if(Route::getCurrentRoute()->uri() == '/')
        <meta content="This Recipe Does Not Exist" property="og:title">

        @php
            $taglines = [
                "This ain't your grandma's cookbook.",
                "The future of cooking is now.",
                "The internet's most unique recipes.",
                "Uncurated culinary creations."
            ]
        @endphp
        <meta content="{!! $taglines[array_rand($taglines)] !!}"
              property="og:description">
    @else
        <meta content="{{ $r->title }}" property="og:title">
        <meta content="{{ count(json_decode($r->ingredients)) }} ingredients, {{ count(json_decode($r->directions)) }} steps."
              property="og:description">
    @endif


    <meta content="thisrecipedoesnotexist.com" property="og:site_name">

    {!! Analytics::render() !!}
    <title>{{ $r->title }}</title>
</head>
<body @if (\Cookie::get('darkmode')) class="dark-mode" @endif>
<div class="text-center col-sm-12 small alert alert-light">
    {{ $total }} recipes created | <a href="{{ $r->id }}" class="text-secondary strong">Permalink</a> | <a
            href="darkmode" class="text-secondary">Dark Mode</a> | <b><a href="/" class="text-secondary">Random</a></b>
</div>
<div class="container">
    <div class="row">
        <div class="content shadow p-3 mb-5 bg-light rounded col-md-8">
            <h1>{{ $r->title }}
            </h1>
            <div class='ing'>
                <h2>Ingredients</h2>
                @foreach (json_decode($r->ingredients) as $ingredient)
                    <p>{{ $ingredient }}</p>
                @endforeach
            </div>
            <div class='dir'>
                <h2>Directions</h2>
                @foreach (json_decode($r->directions) as $direction)
                    <p>{{ $direction }}</p>
                @endforeach
            </div>
        </div>

        <div class="col-md-4 recent-recipes">
            <input placeholder="Search for a Recipe" autocomplete="off" type="text" class="form-control" id="search-rec"
                   name="search-rec">
            <hr>
            <h3>Random Recipes</h3>
            <ul class="list-group">
                @foreach($recent as $key => $re)
                    <a href="{{ $re->id }}"
                       class="list-group-item list-group-item-action"><strong>{{ $re->title }}</strong>
                        <br> {{ count(json_decode($re->ingredients)) }} ingredients <br> {{ $re->timeAgo}}</a>
                @endforeach
            </ul>

            <h3 style="padding-top:20px">Recent Activity</h3>
            <ul class="list-group">
                @foreach($recentComments as $key => $comment)
                    <a href="{{ $comment->recipe->id }}"
                       class="list-group-item list-group-item-action"><strong>{{ $comment->username }} </strong> commented on <strong>{{ $comment->recipe->title }}</strong></a>
                @endforeach
            </ul>


        </div>
    </div>
    @if(count($r->comments)>0)
        <h2>Comments</h2>


        @foreach ($r->comments as $comment)
            <div class="row">

                <div class='content comments shadow p-3 mb-5 bg-light rounded col-md-6'>

                    <b>{{ $comment->username }}</b> writes:<br>

                    <h4 style="padding-left:20px; padding-top:20px;">@for($i=0;$i<$comment->rating;$i++)
                            ⭐
                        @endfor
                    </h4>
                    <blockquote style="padding-left:20px; padding-top:20px;">{{ $comment->body }}</blockquote>
                </div>

            </div>
        @endforeach
    @endif

</div>
<div class='footer'>Recipe generated {{$r->created_at}} | {{ $freshRecipeCount }} fresh recipes left | <strong><a
                class="text-success" href="https://github.com/Hollings/thisrecipedoesnotexist">Github</a> | <a
                class="text-success" href="https://twitter.com/DoesRecipe">Twitter</a></strong>
</div>


<script type="text/javascript">
    var path = "{{ url('api/search') }}";
    $('#search-rec').typeahead({
        minLength: 1,
        items: 20,
        delay: 100,
        afterSelect: function (item) {
            window.location.replace(item.id);
        },
        displayText: function (item) {
            return item.title;
        },
        source: function (query, process) {
            return $.get(path, {query: query}, function (data) {
                return process(data);
            });
        }
    });
</script>
</body>