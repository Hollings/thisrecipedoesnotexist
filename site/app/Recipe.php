<?php

namespace App;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Notifications\Notifiable;
use App\Notifications;
use Illuminate\Queue\Queue;
use NotificationChannels\Twitter\TwitterChannel;

class Recipe extends Model
{
	protected $fillable = ['title','directions','ingredients','temp'];
	use Notifiable;

    /**
     * @return \Illuminate\Database\Eloquent\Relations\HasOne
     */
    public function queuedRecipe(){
		return $this->hasOne(QueuedRecipe::class);
	}

    /**
     * @return \Illuminate\Database\Eloquent\Relations\HasMany
     */
    public function comments(){
	    return $this->hasMany(Comment::class);
    }
}
