<template lang="html">
  <div>
    <div class="search">
      <el-autocomplete
      v-model="selected_classify"
      :fetch-suggestions="querySearchItem"
      prefix-icon="el-icon-search"
      placeholder="搜索景区名称"
      @select="searchItemSelect"
      class='search_box'/>

    </div>

  <div class="recommend_place">
    <p>地区推荐</p>
    <div class='place_wrapper'>
      <div v-for="place in places">
        <!-- <el-tag type="success"> -->
           <!-- <el-button type="success" round> -->
          <router-link tag='el-button' type='success' round :to="{ path: `/tags?place_id=${place.id}` }" class="place_name">
          {{ place.place }}
          </router-link>
        <!-- </el-tag>  -->
      </div>
    </div>
  </div>
  <div class="recommend_class">
    <p>景区推荐</p>
    <div class='classify_wrapper'>
      <Classify v-for="class_ in classes_" :name="class_.classify" page='home' :id='class_.id' :img_path='class_.img_path'/>
    </div>
  </div>
  <!-- <div class="home_wrapper" v-loading="loading2" element-loading-text="加载中">
    <article v-for="item in items">
      <header>
        <router-link :to="{ path: `/article/${item._id}` }" class="home_title">
          {{ item.title }}
        </router-link>
        <div>
          <p class="home_creatAt">{{ item.created_at }}</p>
        </div>
      </header>
      <section v-html="item.contentToMark" class="home_main"></section>
      <footer>
        <router-link
          class="home_readMore"
          :to="{ path: `/article/${item._id}` }"
          >阅读全文>></router-link
        >
      </footer>
    </article>
    <footer class="loadMore" v-if="loadMoreShow">
      <el-button type="primary" :loading="loadMoreFlag" @click="loadMore">{{
        loadMoreText
      }}</el-button>
    </footer>
  </div> -->
  </div>
</template>

<script>
import vhead from "./vheader";
import api from "../../api";
import vfoot from "./vfooter";
import Classify from "./Classify"
export default {
  name: "Home",
  data() {
    return {
      places:[],
      classes_: [],
      selected_classify: '',
      items: [],
      loading2: true,
      loadMoreFlag: false,
      loadMoreText: "加载更多",
      loadMoreShow: false,
      page: 1,
      limit: 10,
    };
  },
  components: {
    vhead,
    vfoot,
    Classify
  },
  methods: {
    // 输入回调
    querySearchItem(queryString, cb) {
      var classes_ = this.classes_
      // 为这个数组中每一个对象加一个value字段
      // 因为autocomplete只识别value字段并在下拉列中显示
      // 多数情况后台数据中是没有value的属性的
      // 要自己建一个数组，给每一项设置value
      for (let i of classes_) {
        i.value = i.classify
        i.label = i.id
      }
      // queryString指输入框中输入的值，若无输入默认显示全部内容，有则显示匹配内容
      var results = queryString ? classes_.filter(this.createStateFilter(queryString)) : classes_
      // 设置回调时间，延迟显示列表，不设置的话直接cb(results)就可以了
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        // 回调函数cb，返回匹配到的内容
        cb(results)
      }, 300 * Math.random())
    },
    // 字母模糊匹配
    createStateFilter(queryString) {
      return (state) => {
        return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },
    // 处理选中项
    searchItemSelect(a) {
      // console.log(this.classes_)
      let classiy_id
      for (let i of this.classes_) {
        if (i.classify == this.selected_classify) {
          classiy_id = i.id
          break
        }
      }
      this.$router.push({ path: `/classify/${classiy_id}` })
    },
    
    
    loadMore() {
      this.loadMoreText = "加载中";
      this.loadMoreFlag = true;
      this.page++;
      // this.loadData(this.page, this.limit);
    },
    loadData(page, limit) {
      api
        .getArticleLists({ page, limit })
        .then(({ data: { code, articleLists, hasNext, hasPrev } }) => {
          if (code == 200) {
            setTimeout(() => {
              this.items = this.items.concat(articleLists);
              this.loading2 = false;
              if (hasNext) {
                this.loadMoreShow = true;
                this.loadMoreFlag = false;
                this.loadMoreText = "加载更多";
              } else {
                this.loadMoreShow = false;
              }
            }, 200);
          }
        });
    },
    loadPlaces(page, limit) {
      api
        .getPlaceList()
        .then((res) => {
          if (res.status == 200) {
            setTimeout(() => {
              this.places = this.places.concat(res.data);
            }, 200);
          }
        });
    },
    loadClasses(page, limit) {
      api
        .getClassify()
        .then((res) => {

          if (res.status == 200) {
            setTimeout(() => {
              this.classes_ = this.classes_.concat(res.data);
              this.loading2 = false;
            }, 200);
          }
        });
    },
  },
  mounted() {
    // 封装成一个方法，与分页获取游记列表类似
    this.$store.dispatch("changeHeadLine", "主页");
    // this.loadData(1, this.limit);
    this.loadPlaces(1, this.limit);
    this.loadClasses(1, this.limit);
  },
};
</script>

<style lang="css" scoped>
h2,
h4 {
  margin: 0;
}
.search {
  width: 60%;
  /* margin-top:-100px; */
  margin-bottom: 100px;
  margin-left:20%;
}


.search_box {
  width: 100%;
}
.classify_wrapper{
  display: flex;
  flex-wrap: wrap;
}

.recommend_place p {
  font-size: 30px;
  text-align: center;
}
.place_wrapper {
  display: flex;
  margin: auto;
  width: 70%;
  flex-wrap: wrap;
}
.place_wrapper div {
  margin: 10px;
}

.recommend_class p {
  font-size: 30px;
  text-align: center;
}

.classify_wrapper {
  margin: auto;
  width: 100%;

}

.place_name {
  width: 100px;
  font-size: 20px;
  height: 50px;
}
.home_wrapper {
  margin: auto;
  list-style: none;
}
.home_wrapper article {
  padding-bottom: 1rem;
  border-bottom: 1px solid #d2d2d2;
  margin-bottom: 2rem;
}
.home_title {
  display: block;
  font-size: 2.6rem;
  font-weight: 400;
  color: #404040;
  padding: 0.8rem 0;
}
.home_creatAt {
  font-family: "Comic Sans MS", curslve, sans-serif;
  font-size: 1.6rem;
  color: #7f8c8d;
  margin: 0;
}

.home_main {
  font-size: 1.6rem;
  color: #34495e;
  line-height: 1.6em;
  /*padding:0.6rem 0;*/
}
footer {
  text-align: right;
}
.home_readMore {
  font-size: 2rem;
  color: #919191;
  font-weight: 600;
}
.loadMore {
  margin: 4rem 0 0 0;
  display: flex;
  display: webkit-flex;
}
.loadMore button {
  cursor: pointer;
  outline: none;
  padding: 1rem;
  margin: auto;
  border-radius: 0.5rem;
  color: rgba(0, 0, 0, 1);
  border: 1px solid #bfcbd9;
  background-color: #f7f7f7;
}
.home_title:hover {
  opacity: 0.5;
}
.home_readMore:hover {
  opacity: 0.6;
}
@media screen and (max-width: 786px) {
  .home_title {
    font-size: 1.8rem;
    line-height: 1.5em;
  }
  .home_creatAt {
    font-size: 1.4rem;
  }
  .loadMore {
    margin: 3rem 0 0.8rem 0;
  }
}
@media screen and (max-width: 480px) {
  .home_main {
    font-size: 1.4rem;
  }
  .home_readMore {
    font-size: 1.8rem;
  }
}
</style>
