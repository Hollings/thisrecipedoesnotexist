<head>
    <style>
    .ing p {
    margin: 0 15px;
    }
    .dir p {
    margin: 15px;
    }
    .dir, .ing{
    margin-top:50px
    }
    .content {
    border: 1px solid #cacaca;
    margin-bottom: 50px;
    }
    .footer {
    text-align: center;
    color: #adb5bd;
    font-size: 10px;
    }
    .recent-recipes {
    font-size: 12px;
    }
    </style>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<div class="text-center col-sm-12 small alert alert-light">
    {{ $total }} recipes created | <a href="{{ $r->id }}" class="text-secondary strong">Permalink</a> | <a href="/" class="text-secondary">Random</a>
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
            <h2>Latest Recipes</h2>
            <ul class="list-group">
                @foreach($recent as $key => $re)
                    <a href="{{ $key }}" class="list-group-item list-group-item-action">{{ $re }}</a>
                @endforeach
            </ul>


           
        </div>
    </div>
</div>
<div class='footer'>Recipe generated with temp of {{ $r->temp }} at {{$r->created_at}}
</div>