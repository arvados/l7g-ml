package com.curoverse.kfang.gettileinfo

import android.content.Context
import android.os.Bundle
import android.os.PersistableBundle
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.view.View
import android.widget.TextView
import android.widget.Toast
import com.curoverse.kfang.gettileinfo.api.TileRetriever
import com.curoverse.kfang.gettileinfo.model.TileInfo
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.disposables.Disposable
import io.reactivex.rxkotlin.subscribeBy
import io.reactivex.schedulers.Schedulers
import kotlinx.android.synthetic.main.activity_main.*
import android.view.inputmethod.InputMethodManager.HIDE_NOT_ALWAYS
import android.content.Context.INPUT_METHOD_SERVICE
import android.view.KeyEvent
import android.view.inputmethod.InputMethodManager
import android.view.KeyEvent.KEYCODE_ENTER
import android.widget.TextView.OnEditorActionListener

class MainActivity : AppCompatActivity() {

    lateinit var allViews: Array<TextView>
    var disposable : Disposable? = null
    var tile : TileInfo? = null

    fun setLoading(loadingState: Boolean) {
        when (loadingState) {
            true -> indeterminateBar.visibility = View.VISIBLE
            false -> indeterminateBar.visibility = View.GONE
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setLoading(false)
        allViews = arrayOf(bp_start, bp_end, base_pair_title, tile_name, to_search, tile_path, tile_step, tile_phase, variants)
        call_api.setOnClickListener {
            val inputManager = getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
            inputManager.hideSoftInputFromWindow(currentFocus!!.windowToken,
                    InputMethodManager.HIDE_NOT_ALWAYS)
            val index = getIndex()
            if (index == null) {
                index_input.error = "Empty input"
            } else {
                allViews.forEach { it.visibility = View.GONE }
                makeCall(index)
            }
        }
        index_input.setOnEditorActionListener { _, _, event ->
            if (event == null) {
                call_api.callOnClick()
                return@setOnEditorActionListener true
            }
            return@setOnEditorActionListener false
        }
        if (savedInstanceState != null) {
            tile = savedInstanceState.getParcelable<TileInfo>(TILE_INFO)
            Log.d("MainActivity", tile.toString())
            if (tile != null) {
                setViews(tile!!)
            }
            val index = savedInstanceState.getInt(TILE_INDEX)
            if (index != -1) {
                index_input.setText(index.toString())
            }
            val currentlySearching = savedInstanceState.getBoolean(CURRENTLY_SEARCHING, false)
            if (currentlySearching) {
                makeCall(index)
            }
        }
    }

    private fun getIndex(): Int? {
        if (index_input.text.toString() == "") {
            return null
        } else {
            return Integer.parseInt(index_input.text.toString())
        }
    }

    override fun onStop() {
        if (disposable != null && !(disposable!!.isDisposed)) { // if currently running
            disposable!!.dispose()
        }
        super.onStop()
    }

    fun makeCall(index: Int) {
        setLoading(true)
        val retriever = TileRetriever()
        if (disposable == null || (disposable != null && disposable!!.isDisposed)) {
            tile = null
            Toast.makeText(this, "Loading...", Toast.LENGTH_SHORT).show()
            disposable = retriever.getTile(index)
                    .observeOn(AndroidSchedulers.mainThread())
                    .subscribeOn(Schedulers.io())
                    .subscribeBy(
                            onNext = { tileInfo: TileInfo ->
                                setViews(tileInfo)
                            },
                            onComplete = { setLoading(false) },
                            onError = { t: Throwable ->
                                setLoading(false)
                                Toast.makeText(this@MainActivity, "Invalid results. Check log.", Toast.LENGTH_SHORT).show()
                                Log.d("MainActivity", "Error:", t)
                            }
                    )
        }
    }

    override fun onSaveInstanceState(outState: Bundle?) {
        super.onSaveInstanceState(outState)
        if (disposable != null && !(disposable!!.isDisposed)) { // is currently running
            Log.d("MainActivity", "disposed")
            outState?.putBoolean(CURRENTLY_SEARCHING, true)
        }
        outState?.putParcelable(TILE_INFO, tile)
        outState?.putInt(TILE_INDEX, getIndex() ?: -1)
    }

    private fun setViews(info: TileInfo) {
        tile = info
        allViews.forEach { it.visibility = View.VISIBLE }
        bp_start.text = info.base_pair_start
        bp_end.text = info.base_pair_end
        tile_name.text = info.name
        to_search.text = resources.getString(R.string.to_search_list, info.search.toString())
        tile_path.text = resources.getString(R.string.tile_path_s, info.tile_path)
        tile_step.text = resources.getString(R.string.tile_step_s, info.tile_step)
        tile_phase.text = resources.getString(R.string.tile_phase_s, info.tile_phase)
        variants.text = getVariants(info.variants)
    }

    private fun getVariants(variants: ArrayList<String>): String {
        val builder = StringBuilder()
        variants.forEach {
            builder.append(it + '\n')
        }
        return builder.toString()
    }

    companion object {
        val TILE_INFO = "tile.info"
        val CURRENTLY_SEARCHING = "tile.searching"
        val TILE_INDEX = "tile.index"
    }
}
