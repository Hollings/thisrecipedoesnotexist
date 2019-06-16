<?php

namespace App;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Notifications\Notifiable;
use App\Notifications;
use NotificationChannels\Twitter\TwitterChannel;

class Recipe extends Model
{
	protected $fillable = ['title','directions','ingredients','temp'];
	use Notifiable;    

	public function queuedRecipe(){
		return $this->hasOne('App\QueuedRecipe');
	}
}
