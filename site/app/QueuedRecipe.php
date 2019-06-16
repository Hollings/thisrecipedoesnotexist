<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class QueuedRecipe extends Model
{
    protected $fillable = ['title', 'requested_by_name', 'requested_by_id', 'status', 'mention_id', 'recipe_id'];
    public function recipe(){
    	return $this->belongsTo('App\Recipe');
    }
}
