<?php

namespace App\Http\Controllers;

use App\Recipe;
use App\QueuedRecipe;
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
        $freshRecipeCount = Recipe::where('views', 0)->count();
        if (!$r) {
            $r = Recipe::inRandomOrder()->first();
        }
        $recent = $this->getRecentRecipes(10);
        $r->views = $r->views+1;
        $r->save();
        $total = Recipe::count();
        return View::make('home', array('r' => $r, 'total'=>$total, 'recent'=>$recent, 'freshRecipeCount'=>$freshRecipeCount));
    }

   public function view(Recipe $r){
        $recent = $this->getRecentRecipes(10);
        $r->views = $r->views+1;
        $r->save = true;
        $r->save();
        $total = Recipe::count();
        $freshRecipeCount = Recipe::where('views', 0)->count();

        return View::make('home', array('r' => $r, 'total'=>$total, 'recent'=>$recent, 'freshRecipeCount'=>$freshRecipeCount));
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
    $data = $request->all();

    // Yeah I know... I'll add Passport later
    if (Hash::check($data['password'], '$2y$10$y/TJW50eL4loeni.h7ddv.isQZ8SDutOuhst8XGyDm2cuCxRHpb1q')) {
         $r = Recipe::create($data);
         if (isset($data['queue_id']) && $data['queue_id'] != 0) {
            QueuedRecipe::find($data['queue_id'])->update(['status'=>'generated', 'recipe_id'=>$r->id]);

         }
         return $r->id;
    }else{
        return "failed";
    }
   }

   public function getRecipeRaw(){

        $r = Recipe::whereHas('queuedRecipe', function($query){
            $query->where('status', 'generated');
        })->with('queuedRecipe')->first();

        if ($r) {
            $qr = $r->queuedRecipe;
            $qr->status='complete';
            $qr->save();
            return $r;
        }else{
            return Recipe::inRandomOrder()->first();
        }
   }

    public function search(Request  $request)
    {
        $result=Recipe::where('title', 'LIKE', "%{$request->input('query')}%")->select('id','title')->get();
        return response()->json($result);
    }

    public function toggleDark(Request $request){
        if ($request->cookie('darkmode')) {
             \Cookie::queue(\Cookie::forget('darkmode'));
        }else{
            \Cookie::queue("darkmode", "1", 99999999);
        }
        return back();
    }


    // Queued recipe methods
    public function queueRecipe(Request $request){
        if (!QueuedRecipe::where('mention_id', $request->mention_id)->exists()) {
            $q = QueuedRecipe::create($request->all() + ['status'=>'queued']);
            return $q->id;
        }
    }

    public function getNextQueuedRecipe(){
        return QueuedRecipe::where('status','queued')->first() ?? [];
    }

}
