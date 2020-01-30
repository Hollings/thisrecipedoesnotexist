<?php

namespace App\Http\Controllers;

use App\Comment;
use App\Recipe;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class CommentController extends Controller
{
    public function save(Request $request) {

        // I really should get some actual auth
        if (!Hash::check($request['password'], '$2y$10$y/TJW50eL4loeni.h7ddv.isQZ8SDutOuhst8XGyDm2cuCxRHpb1q')) {
            return true;
        }


        dump($request->all());
        $comment = Comment::make($request->all());

        if ($request->recipe_id) {
            $recipe = Recipe::find($request->recipe_id);
        }else{
            $recipe = Recipe::inRandomOrder()->first();
        }

        if(!$recipe){
            dump("no recipe");
            return true;
        }
        dump($recipe->id);

        $comment->recipe()->associate($recipe)->save();

        return "ok";
    }
}
