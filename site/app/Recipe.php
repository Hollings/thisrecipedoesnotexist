<?php

namespace App;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Notifications\Notifiable;
use App\Notifications;
use NotificationChannels\Twitter\TwitterChannel;

class Recipe extends Model
{
	use Notifiable;    
}
