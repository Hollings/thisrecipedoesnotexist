<?php

namespace App\Http\Controllers;

use App\Recipe;
use View;
use Illuminate\Http\Request;
use Carbon;
use Hash;

class RecipeController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $r = Recipe::where('views', 0)->first();
        if (!$r) {
            $r = Recipe::inRandomOrder()->first();
        }
        $recent = $this->getRecentRecipes(10);
        $r->views = $r->views+1;
        $r->save();
        $total = Recipe::count();
        return View::make('home', array('r' => $r, 'total'=>$total, 'recent'=>$recent));
    }

   public function view(Recipe $r){
        $recent = $this->getRecentRecipes(10);
        $r->views = $r->views+1;
        $r->save = true;
        $r->save();
        $total = Recipe::count();
        return View::make('home', array('r' => $r, 'total'=>$total, 'recent'=>$recent));
   }


   private function getRecentRecipes($n){
        $recents = Recipe::latest()->take($n)->select('title','id','created_at')->get();
        foreach ($recents as $key => &$recent) {
            $date = $recent->created_at->format('d-m-Y H:i:s');
            $recent->timeAgo = Carbon\Carbon::parse($date)->diffForHumans();
        }
        return $recents;
   }

   public function saveRecipe(Request $request){

    // Yeah I know... I'll add Passport later
    if (Hash::check($request->password, '$2y$10$y/TJW50eL4loeni.h7ddv.isQZ8SDutOuhst8XGyDm2cuCxRHpb1q')) {
         Recipe::create($request->all());
         return "success";
    }else{
        return "failed";
    }
   }

   public function getRecipeRaw(){
        return Recipe::inRandomOrder()->first();
   }

    public function search(Request  $request)
    {
        $result=Recipe::where('title', 'LIKE', "%{$request->input('query')}%")->select('id','title')->get();
        return response()->json($result);
    }
}
