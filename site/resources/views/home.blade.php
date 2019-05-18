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
    .container {
    border: 1px solid #cacaca;
    margin-top: 50px;
    margin-bottom: 50px;
    }
    .footer {
    text-align: center;
    color: #adb5bd;
    font-size: 10px;
    }
    </style>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>




<div class="text-center col-sm-12 small alert alert-light">
    {{ $total }} recipes created | <a href="{{ $r->id }}" class="text-secondary">Permalink</a>
</div>
<div class="container shadow p-3 mb-5 bg-light rounded">
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

<div class='footer'>Recipe generated with temp of {{ $r->temp }} at {{$r->created_at}}
</div>